import os

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.logging import LoggingIntegration


def configure_monitoring() -> None:
    """Enable error reporting when a GlitchTip DSN is configured."""
    load_dotenv()
    dsn = os.getenv("SENTRY_DSN")
    if not dsn:
        return

    sentry_sdk.init(
        dsn=dsn,
        environment=os.getenv("SENTRY_ENVIRONMENT", "development"),
        release=os.getenv("SENTRY_RELEASE") or None,
        integrations=[LoggingIntegration(level=None, event_level=None)],
        traces_sample_rate=0,
        auto_session_tracking=False,
        include_local_variables=False,
        max_request_body_size="never",
        max_breadcrumbs=0,
    )
    sentry_sdk.set_tag("service", "bot")
