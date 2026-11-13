import json
import os
from unittest.mock import patch

import sentry_sdk
from django.test import SimpleTestCase, override_settings
from django.urls import path
from sentry_sdk.transport import Transport

from backend.monitoring import configure_monitoring


def failing_view(request):
    raise RuntimeError("Backend monitoring test")


urlpatterns = [path("monitoring-test/", failing_view)]


class RecordingTransport(Transport):
    def __init__(self):
        super().__init__()
        self.events = []

    def capture_envelope(self, envelope):
        for item in envelope.items:
            if item.type == "event":
                self.events.append(item.payload.json)


@override_settings(ROOT_URLCONF=__name__)
class MonitoringTests(SimpleTestCase):
    def test_unhandled_view_error_is_reported_without_request_body_or_locals(self):
        previous_client = sentry_sdk.get_client()
        with sentry_sdk.isolation_scope():
            with patch.dict(os.environ, {"SENTRY_DSN": "http://key@localhost/1"}):
                configure_monitoring()
            transport = RecordingTransport()
            client = sentry_sdk.get_client()
            client.transport.kill()
            client.transport = transport
            try:
                with self.assertRaisesMessage(RuntimeError, "Backend monitoring test"):
                    self.client.post(
                        "/monitoring-test/",
                        {"private": "secret-request-content"},
                        HTTP_AUTHORIZATION="Bearer secret-auth-token",
                    )
                self.assertEqual(len(transport.events), 1)
                event = transport.events[0]
                self.assertEqual(event["tags"]["service"], "backend")
                self.assertEqual(
                    event["exception"]["values"][-1]["type"], "RuntimeError"
                )
                serialized = json.dumps(event)
                self.assertNotIn("secret-request-content", serialized)
                self.assertNotIn("secret-auth-token", serialized)
                self.assertFalse(event.get("breadcrumbs", {}).get("values"))
                for value in event["exception"]["values"]:
                    for frame in value.get("stacktrace", {}).get("frames", []):
                        self.assertNotIn("vars", frame)
            finally:
                client.close()
                sentry_sdk.get_global_scope().set_client(previous_client)
