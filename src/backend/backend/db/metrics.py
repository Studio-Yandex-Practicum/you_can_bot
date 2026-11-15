"""Bounded SQL error totals alongside django-prometheus's type breakdown."""

from prometheus_client import Counter

QUERY_ERRORS = Counter(
    "django_db_query_errors_total",
    "Failed SQL executions by database, including the first error type seen.",
    ["alias", "vendor"],
)


class QueryErrorMetricsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query_error_counter = QUERY_ERRORS.labels(self.alias, self.vendor)
        self.query_error_counter.inc(0)


def count_query_errors(cursor_class, counter):
    class ErrorCountingCursor(cursor_class):
        def execute(self, *args, **kwargs):
            with counter.count_exceptions():
                return super().execute(*args, **kwargs)

        def executemany(self, *args, **kwargs):
            with counter.count_exceptions():
                return super().executemany(*args, **kwargs)

    return ErrorCountingCursor
