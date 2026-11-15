from django_prometheus.db.backends.postgresql.base import (
    DatabaseWrapper as PrometheusDatabaseWrapper,
)

from backend.db.metrics import QueryErrorMetricsMixin, count_query_errors


class DatabaseWrapper(QueryErrorMetricsMixin, PrometheusDatabaseWrapper):
    def get_connection_params(self):
        params = super().get_connection_params()
        params["cursor_factory"] = count_query_errors(
            params["cursor_factory"], self.query_error_counter
        )
        return params
