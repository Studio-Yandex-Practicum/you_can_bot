import io
import json
import os
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.db import DatabaseError, OperationalError, connections, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.test import RequestFactory, SimpleTestCase, TestCase, override_settings
from django.urls import path
from prometheus_client import REGISTRY

from backend.metrics import AfterMiddleware, BeforeMiddleware
from backend.metrics_wsgi import MonitoringApplication, database_ready


def session_redirect(request):
    request.session["metrics-test"] = True
    return HttpResponseRedirect("/admin/")


def server_error(request):
    return HttpResponse(status=500)


urlpatterns = [
    path("session-redirect/", session_redirect),
    path("server-error/", server_error),
]


class FirstErrorBurstTests(SimpleTestCase):
    def test_first_bursts_have_aggregate_zero_baselines(self):
        code = textwrap.dedent(
            """
            import json, os
            import django
            django.setup()
            from django.conf import settings
            settings.DATABASES['default']['NAME'] = ':memory:'
            from django.core.wsgi import get_wsgi_application
            from django.db import DatabaseError, connections
            from django.test import Client, override_settings
            from prometheus_client import REGISTRY, CollectorRegistry, multiprocess

            get_wsgi_application()
            def snapshot():
                registry = REGISTRY
                if 'PROMETHEUS_MULTIPROC_DIR' in os.environ:
                    registry = CollectorRegistry()
                    multiprocess.MultiProcessCollector(registry)
                return {
                    'http': registry.get_sample_value(
                        'django_http_server_errors_total'
                    ),
                    'sql': registry.get_sample_value(
                        'django_db_query_errors_total',
                        {'alias': 'default', 'vendor': 'sqlite'},
                    ),
                }
            before = snapshot()
            with override_settings(ROOT_URLCONF='backend.test_metrics'):
                client = Client()
                for _ in range(5):
                    assert client.get('/server-error/').status_code == 500
            for _ in range(3):
                try:
                    with connections['default'].cursor() as cursor:
                        cursor.execute('SELECT FROM')
                except DatabaseError:
                    pass
            detailed = {
                'http': sum(
                    sample.value for metric in REGISTRY.collect()
                    for sample in metric.samples
                    if sample.name == 'django_http_responses_total_by_status_total'
                    and sample.labels['status'] == '500'
                ),
                'sql': REGISTRY.get_sample_value(
                    'django_db_errors_total',
                    {
                        'alias': 'default', 'vendor': 'sqlite',
                        'type': 'OperationalError',
                    },
                ),
            }
            print(json.dumps({
                'before': before, 'after': snapshot(), 'detailed': detailed,
            }))
            """
        )
        environment = os.environ.copy()
        environment.pop("PROMETHEUS_MULTIPROC_DIR", None)
        environment.pop("prometheus_multiproc_dir", None)
        environment.update(
            DJANGO_SETTINGS_MODULE="backend.settings",
            PROMETHEUS_ENABLED="true",
            NEED_SQLITE="true",
            SENTRY_DSN="",
        )
        for use_multiprocess in (False, True):
            with tempfile.TemporaryDirectory(
                prefix="backend-burst-metrics-"
            ) as directory:
                self.assertEqual(
                    Path(directory).resolve().parent,
                    Path(tempfile.gettempdir()).resolve(),
                )
                if use_multiprocess:
                    environment["PROMETHEUS_MULTIPROC_DIR"] = directory
                for worker in range(2 if use_multiprocess else 1):
                    process = subprocess.run(
                        [sys.executable, "-c", code],
                        cwd=Path(__file__).resolve().parent.parent,
                        env=environment,
                        capture_output=True,
                        text=True,
                        timeout=20,
                    )
                    self.assertEqual(process.returncode, 0, process.stderr)
                    observed = json.loads(process.stdout)
                    self.assertEqual(observed["detailed"], {"http": 5, "sql": 3})
                    for metric, expected in (("http", 5), ("sql", 3)):
                        with self.subTest(
                            metric=metric, multiprocess=use_multiprocess, worker=worker
                        ):
                            self.assertEqual(
                                observed["before"][metric], expected * worker
                            )
                            self.assertEqual(
                                observed["after"][metric], expected * (worker + 1)
                            )


class FinalResponseMetricsTests(TestCase):
    def setUp(self):
        if not settings.PROMETHEUS_ENABLED:
            self.skipTest("Run with PROMETHEUS_ENABLED=true")

    def response_count(self, status):
        # This is the counter queried by the HTTP dashboard and 5xx alerts.
        return sum(
            sample.value
            for metric in REGISTRY.collect()
            for sample in metric.samples
            if sample.name == "django_http_responses_total_by_status_view_method_total"
            and sample.labels["status"] == str(status)
        )

    def test_common_middleware_redirect_records_final_301_instead_of_404(self):
        redirects, missing = self.response_count(301), self.response_count(404)
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(self.response_count(301), redirects + 1)
        self.assertEqual(self.response_count(404), missing)

    @override_settings(
        ROOT_URLCONF=__name__, SESSION_ENGINE="django.contrib.sessions.backends.db"
    )
    def test_session_response_failure_records_final_500_instead_of_302(self):
        failures, redirects = self.response_count(500), self.response_count(302)
        self.client.raise_request_exception = False
        with patch(
            "django.contrib.sessions.backends.db.SessionStore.save",
            side_effect=OperationalError("Synthetic session write failure"),
        ):
            response = self.client.get("/session-redirect/")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(self.response_count(500), failures + 1)
        self.assertEqual(self.response_count(302), redirects)

    @override_settings(SECURE_SSL_REDIRECT=True)
    def test_security_middleware_short_circuit_is_counted_once(self):
        before = self.response_count(301)
        response = self.client.get("/api/v1/")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(self.response_count(301), before + 1)


class ConnectionMetricsTests(SimpleTestCase):
    def test_first_connection_failure_has_a_zero_baseline(self):
        # A fresh process ensures no earlier test has created this label set.
        code = textwrap.dedent(
            """
            import json, os
            from unittest.mock import patch
            import django
            django.setup()
            from django.core.wsgi import get_wsgi_application
            from django.db import OperationalError, connections
            from prometheus_client import REGISTRY, CollectorRegistry, multiprocess

            def read_counter():
                registry = REGISTRY
                if 'PROMETHEUS_MULTIPROC_DIR' in os.environ:
                    registry = CollectorRegistry()
                    multiprocess.MultiProcessCollector(registry)
                return registry.get_sample_value(
                    'django_db_new_connection_errors_total',
                    {'alias': 'default', 'vendor': 'postgresql'},
                )

            method = (
                'django.db.backends.postgresql.base.'
                'DatabaseWrapper.get_new_connection'
            )
            with patch(method) as connect:
                get_wsgi_application()
                connect.assert_not_called()
            before = read_counter()
            database = connections['default']
            with patch(
                method, side_effect=OperationalError('Synthetic failure')
            ) as connect:
                try:
                    database.get_new_connection(database.get_connection_params())
                except OperationalError:
                    pass
                connect.assert_called_once()
            after = read_counter()
            get_wsgi_application()
            repeated = read_counter()
            print(json.dumps({'before': before, 'after': after, 'repeated': repeated}))
            """
        )
        environment = os.environ.copy()
        environment.pop("NEED_SQLITE", None)
        environment.pop("PROMETHEUS_MULTIPROC_DIR", None)
        environment.pop("prometheus_multiproc_dir", None)
        environment.update(
            DJANGO_SETTINGS_MODULE="backend.settings",
            PROMETHEUS_ENABLED="true",
            DB_ENGINE="django.db.backends.postgresql",
            SENTRY_DSN="",
        )
        for use_multiprocess in (False, True):
            with self.subTest(multiprocess=use_multiprocess):
                with tempfile.TemporaryDirectory(
                    prefix="backend-metrics-"
                ) as directory:
                    self.assertEqual(
                        Path(directory).resolve().parent,
                        Path(tempfile.gettempdir()).resolve(),
                    )
                    if use_multiprocess:
                        environment["PROMETHEUS_MULTIPROC_DIR"] = directory
                    for worker in range(2 if use_multiprocess else 1):
                        process = subprocess.run(
                            [sys.executable, "-c", code],
                            cwd=Path(__file__).resolve().parent.parent,
                            env=environment,
                            capture_output=True,
                            text=True,
                            timeout=20,
                        )
                        self.assertEqual(process.returncode, 0, process.stderr)
                        observed = json.loads(process.stdout)
                        self.assertEqual(
                            observed,
                            {
                                "before": worker,
                                "after": worker + 1,
                                "repeated": worker + 1,
                            },
                        )


class ListenerTests(SimpleTestCase):
    def call(self, port, path, method="GET", **headers):
        calls = []
        app = MonitoringApplication(lambda env, start: [b"application"])
        body = app(
            {
                "SERVER_PORT": port,
                "PATH_INFO": path,
                "REQUEST_METHOD": method,
                "wsgi.input": io.BytesIO(),
                **headers,
            },
            lambda status, response_headers: calls.append(status),
        )
        return b"".join(body), calls

    def test_public_socket_cannot_select_monitoring_with_headers(self):
        for request_path in ("/metrics", "/health/ready"):
            body, statuses = self.call(
                "8000",
                request_path,
                HTTP_HOST="localhost:8002",
                HTTP_X_FORWARDED_PORT="8002",
            )
            self.assertEqual(body, b"application")
            self.assertEqual(statuses, [])

    def test_private_socket_is_not_a_second_application_entrypoint(self):
        self.assertEqual(self.call("8002", "/api/v1/")[1], ["404 Not Found"])
        self.assertEqual(
            self.call("8002", "/metrics", "POST")[1], ["405 Method Not Allowed"]
        )

    def test_readiness_reflects_database_failure_without_details(self):
        with patch("backend.metrics_wsgi.database_ready", return_value=False):
            self.assertEqual(
                self.call("8002", "/health/ready"),
                (b'{"ready": false}', ["503 Service Unavailable"]),
            )


class MiddlewareTests(SimpleTestCase):
    def test_failed_request_contributes_one_latency_observation(self):
        request = RequestFactory().get("/failed/")
        middleware = AfterMiddleware(lambda request: HttpResponse())
        labels = {"view": "<unnamed view>", "method": "GET"}
        name = "django_http_requests_latency_seconds_by_view_method_count"
        before = REGISTRY.get_sample_value(name, labels) or 0
        middleware.process_request(request)
        middleware.process_exception(request, RuntimeError("synthetic failure"))
        middleware.process_response(request, HttpResponse(status=500))
        self.assertEqual(REGISTRY.get_sample_value(name, labels), before + 1)

    def test_latency_labels_normalize_unknown_methods_and_omit_path(self):
        request = RequestFactory().get("/users/123456/private/?token=secret")
        request.method = "UNBOUNDED-METHOD"
        middleware = AfterMiddleware(lambda request: HttpResponse())
        middleware.process_request(request)
        middleware.process_response(request, HttpResponse(status=404))
        samples = [
            sample
            for metric in REGISTRY.collect()
            for sample in metric.samples
            if sample.name
            == "django_http_requests_latency_seconds_by_view_method_count"
        ]
        self.assertTrue(any(s.labels["method"] == "<invalid method>" for s in samples))
        self.assertFalse(
            any("123456" in str(s.labels) or "secret" in str(s.labels) for s in samples)
        )

    def test_in_progress_returns_to_baseline_after_response(self):
        name = "django_http_requests_in_progress"
        before = REGISTRY.get_sample_value(name) or 0
        request = RequestFactory().get("/")
        middleware = BeforeMiddleware(lambda request: HttpResponse())
        middleware.process_request(request)
        self.assertEqual(REGISTRY.get_sample_value(name), before + 1)
        middleware.process_response(request, HttpResponse(status=500))
        self.assertEqual(REGISTRY.get_sample_value(name), before)


class ReadinessTests(TestCase):
    def test_readiness_uses_its_own_connection(self):
        self.assertTrue(database_ready())
        self.assertTrue(connections["default"].is_usable())

    def test_database_error_returns_not_ready(self):
        with patch("backend.metrics_wsgi.connections") as databases:
            database = databases.__getitem__.return_value.copy.return_value
            database.cursor.side_effect = RuntimeError("private database details")
            self.assertFalse(database_ready())
            database.close.assert_called_once()


@override_settings(PROMETHEUS_ENABLED=True)
class SQLMetricsTests(TestCase):
    def test_failed_execute_and_executemany_are_counted_once(self):
        if not connections["default"].settings_dict["ENGINE"].startswith("backend.db."):
            self.skipTest("Run with PROMETHEUS_ENABLED=true")
        labels = {"alias": "default", "vendor": connections["default"].vendor}
        for method in ("execute", "executemany"):
            with self.subTest(method=method):
                before = REGISTRY.get_sample_value(
                    "django_db_query_errors_total", labels
                )
                with self.assertRaises(DatabaseError), transaction.atomic():
                    with connections["default"].cursor() as cursor:
                        if method == "execute":
                            cursor.execute("SELECT FROM")
                        else:
                            cursor.executemany("SELECT FROM", [()])
                self.assertEqual(
                    REGISTRY.get_sample_value("django_db_query_errors_total", labels),
                    before + 1,
                )

    def test_instrumented_database_counts_queries(self):
        if not connections["default"].settings_dict["ENGINE"].startswith("backend.db."):
            self.skipTest(
                "Run with PROMETHEUS_ENABLED=true to check SQL instrumentation"
            )
        labels = {"alias": "default", "vendor": connections["default"].vendor}
        name = "django_db_execute_total"
        before = REGISTRY.get_sample_value(name, labels) or 0
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1")
        self.assertGreater(REGISTRY.get_sample_value(name, labels), before)
