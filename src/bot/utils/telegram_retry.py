import asyncio
import logging
from typing import Optional

from telegram._utils.types import ODVInput
from telegram.error import BadRequest, NetworkError
from telegram.request import HTTPXRequest
from telegram.request._baserequest import BaseRequest
from telegram.request._requestdata import RequestData

_LOGGER = logging.getLogger(__name__)

DO_REQUEST_MAX_ATTEMPTS = 3
DO_REQUEST_INITIAL_DELAY_SECONDS = 1.0


class RetryingHTTPXRequest(HTTPXRequest):
    """HTTPXRequest that retries transient NetworkError failures.

    RetryAfter is raised one layer above (in BaseRequest.post) and is handled
    by AIORateLimiter, so it is not retried here to avoid double-retry.
    BadRequest is also raised above do_request and never reaches this layer.
    """

    async def do_request(
        self,
        url: str,
        method: str,
        request_data: Optional[RequestData] = None,
        read_timeout: ODVInput[float] = BaseRequest.DEFAULT_NONE,
        write_timeout: ODVInput[float] = BaseRequest.DEFAULT_NONE,
        connect_timeout: ODVInput[float] = BaseRequest.DEFAULT_NONE,
        pool_timeout: ODVInput[float] = BaseRequest.DEFAULT_NONE,
    ) -> tuple[int, bytes]:
        for attempt in range(1, DO_REQUEST_MAX_ATTEMPTS + 1):
            try:
                return await super().do_request(
                    url=url,
                    method=method,
                    request_data=request_data,
                    read_timeout=read_timeout,
                    write_timeout=write_timeout,
                    connect_timeout=connect_timeout,
                    pool_timeout=pool_timeout,
                )
            except BadRequest:
                raise
            except NetworkError:
                if attempt == DO_REQUEST_MAX_ATTEMPTS:
                    _LOGGER.exception(
                        "Network error on %s %s after %d attempts",
                        method,
                        _redact_url(url),
                        DO_REQUEST_MAX_ATTEMPTS,
                    )
                    raise
                delay = DO_REQUEST_INITIAL_DELAY_SECONDS * 2 ** (attempt - 1)
                _LOGGER.warning(
                    "Network error on %s %s (attempt %d/%d), retrying in %.1fs",
                    method,
                    _redact_url(url),
                    attempt,
                    DO_REQUEST_MAX_ATTEMPTS,
                    delay,
                )
                await asyncio.sleep(delay)


def _redact_url(url: str) -> str:
    return url.rsplit("/", 1)[-1] or url
