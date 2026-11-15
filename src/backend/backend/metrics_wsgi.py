"""Serve monitoring endpoints exclusively on Gunicorn's private socket."""

import json

from django.db import connections
from prometheus_client import CollectorRegistry, make_wsgi_app, multiprocess

METRICS_PORT = "8002"


def database_ready():
    # A separate short-lived connection bounds probe time and keeps health-query
    # traffic out of the application's default-alias SQL metrics.
    database = connections["default"].copy(alias="monitoring")
    if database.vendor == "postgresql":
        database.settings_dict["OPTIONS"] = {
            **database.settings_dict.get("OPTIONS", {}),
            "connect_timeout": 3,
            "options": (
                database.settings_dict.get("OPTIONS", {}).get("options", "")
                + " -c statement_timeout=2000"
            ),
        }
    try:
        with database.cursor() as cursor:
            cursor.execute("SELECT 1")
            return cursor.fetchone() == (1,)
    except Exception:
        return False
    finally:
        database.close()


def response(start_response, status, body):
    start_response(
        status,
        [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(body))),
            ("Cache-Control", "no-store"),
        ],
    )
    return [body]


class MonitoringApplication:
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        # SERVER_PORT comes from the listening socket, never from HTTP Host.
        if environ.get("SERVER_PORT") != METRICS_PORT:
            return self.application(environ, start_response)
        if environ.get("REQUEST_METHOD") != "GET":
            return response(start_response, "405 Method Not Allowed", b"{}")
        if environ.get("PATH_INFO") == "/metrics":
            registry = CollectorRegistry()
            multiprocess.MultiProcessCollector(registry)
            return make_wsgi_app(registry)(environ, start_response)
        if environ.get("PATH_INFO") == "/health/ready":
            ready = database_ready()
            body = json.dumps({"ready": ready}).encode("utf-8")
            return response(
                start_response, "200 OK" if ready else "503 Service Unavailable", body
            )
        return response(start_response, "404 Not Found", b"{}")
