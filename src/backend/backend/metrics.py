"""Django telemetry without request paths, SQL text or user identifiers."""

from django.db import connections
from django_prometheus.db import connection_errors_total
from django_prometheus.middleware import (
    PrometheusAfterMiddleware,
    PrometheusBeforeMiddleware,
)
from prometheus_client import Counter, Gauge

SERVER_ERRORS = Counter(
    "django_http_server_errors_total",
    "Final HTTP 5xx responses across all handlers and methods.",
)

IN_PROGRESS = Gauge(
    "django_http_requests_in_progress",
    "Requests currently handled by live Gunicorn workers.",
    multiprocess_mode="livesum",
)
WORKERS = Gauge(
    "django_gunicorn_workers",
    "Live initialized Gunicorn workers.",
    multiprocess_mode="livesum",
)


class BeforeMiddleware(PrometheusBeforeMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Publish zero before the first connection attempt so increase() can
        # observe a single failure. inc(0) preserves existing worker counters.
        for database in connections.all():
            connection_errors_total.labels(database.alias, database.vendor).inc(0)

    def process_request(self, request):
        super().process_request(request)
        IN_PROGRESS.inc()
        request.prometheus_in_progress = True

    def process_response(self, request, response):
        try:
            return super().process_response(request, response)
        finally:
            if getattr(request, "prometheus_in_progress", False):
                IN_PROGRESS.dec()


class AfterMiddleware(PrometheusAfterMiddleware):
    def process_response(self, request, response):
        response = super().process_response(request, response)
        if 500 <= response.status_code < 600:
            SERVER_ERRORS.inc()
        return response

    def label_metric(self, metric, request, response=None, **labels):
        # The library normalizes method counters but not latency labels.
        if "method" in labels:
            labels["method"] = self._method(request)
        return super().label_metric(metric, request, response, **labels)

    def process_exception(self, request, exception):
        # Django still runs process_response for the generated 500 response.
        # Observe latency there once, rather than twice for failed requests.
        self.metrics.exceptions_by_type.labels(type=type(exception).__name__).inc()
        self.metrics.exceptions_by_view.labels(view=self._get_view_name(request)).inc()
