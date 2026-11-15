from django_prometheus.db.backends.sqlite3.base import (
    DatabaseWrapper as PrometheusDatabaseWrapper,
)

from backend.db.metrics import QueryErrorMetricsMixin, count_query_errors


class DatabaseWrapper(QueryErrorMetricsMixin, PrometheusDatabaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CURSOR_CLASS = count_query_errors(
            self.CURSOR_CLASS, self.query_error_counter
        )
