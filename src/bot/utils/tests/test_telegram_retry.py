from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

from telegram.error import BadRequest, NetworkError, RetryAfter

from utils.telegram_retry import (
    DO_REQUEST_MAX_ATTEMPTS,
    RetryingHTTPXRequest,
)


def _new_request():
    request = RetryingHTTPXRequest.__new__(RetryingHTTPXRequest)
    return request


class RetryingHTTPXRequestTests(IsolatedAsyncioTestCase):
    """Retry behaviour of RetryingHTTPXRequest.do_request."""

    @patch("utils.telegram_retry.asyncio.sleep", new=AsyncMock())
    @patch("telegram.request.HTTPXRequest.do_request")
    async def test_returns_payload_on_first_success(self, parent_do_request):
        parent_do_request.return_value = (200, b"ok")
        request = _new_request()

        code, payload = await request.do_request(url="https://x", method="POST")

        self.assertEqual((code, payload), (200, b"ok"))
        parent_do_request.assert_awaited_once()

    @patch("utils.telegram_retry.asyncio.sleep", new=AsyncMock())
    @patch("telegram.request.HTTPXRequest.do_request")
    async def test_retries_network_error_then_succeeds(self, parent_do_request):
        parent_do_request.side_effect = [NetworkError("flap"), (200, b"ok")]
        request = _new_request()

        code, payload = await request.do_request(url="https://x", method="POST")

        self.assertEqual((code, payload), (200, b"ok"))
        self.assertEqual(parent_do_request.await_count, 2)

    @patch("utils.telegram_retry.asyncio.sleep", new=AsyncMock())
    @patch("telegram.request.HTTPXRequest.do_request")
    async def test_reraises_after_max_attempts(self, parent_do_request):
        parent_do_request.side_effect = NetworkError("down")
        request = _new_request()

        with self.assertRaises(NetworkError):
            await request.do_request(url="https://x", method="POST")
        self.assertEqual(parent_do_request.await_count, DO_REQUEST_MAX_ATTEMPTS)

    @patch("utils.telegram_retry.asyncio.sleep", new=AsyncMock())
    @patch("telegram.request.HTTPXRequest.do_request")
    async def test_does_not_retry_bad_request(self, parent_do_request):
        parent_do_request.side_effect = BadRequest("Can't parse entities")
        request = _new_request()

        with self.assertRaises(BadRequest):
            await request.do_request(url="https://x", method="POST")
        parent_do_request.assert_awaited_once()

    @patch("utils.telegram_retry.asyncio.sleep", new=AsyncMock())
    @patch("telegram.request.HTTPXRequest.do_request")
    async def test_does_not_retry_retry_after(self, parent_do_request):
        parent_do_request.side_effect = RetryAfter(5)
        request = _new_request()

        with self.assertRaises(RetryAfter):
            await request.do_request(url="https://x", method="POST")
        parent_do_request.assert_awaited_once()

    @patch("utils.telegram_retry.asyncio.sleep", new=AsyncMock())
    @patch("telegram.request.HTTPXRequest.do_request")
    async def test_does_not_leak_token_in_logs(self, parent_do_request):
        parent_do_request.side_effect = [NetworkError("flap"), (200, b"ok")]
        request = _new_request()
        token_url = (
            "https://api.telegram.org/bot7123456789:AAA-secret-token-XYZ/getMe"
        )

        with self.assertLogs("utils.telegram_retry", level="WARNING") as captured:
            await request.do_request(url=token_url, method="POST")

        joined = "\n".join(captured.output)
        self.assertNotIn("AAA-secret-token-XYZ", joined)
        self.assertNotIn("7123456789", joined)
        self.assertIn("getMe", joined)

    @patch("utils.telegram_retry.asyncio.sleep", new=AsyncMock())
    @patch("telegram.request.HTTPXRequest.do_request")
    async def test_does_not_leak_token_on_exhaustion(self, parent_do_request):
        parent_do_request.side_effect = NetworkError("down")
        request = _new_request()
        token_url = (
            "https://api.telegram.org/bot7123456789:AAA-secret-token-XYZ/sendMessage"
        )

        with self.assertLogs("utils.telegram_retry", level="ERROR") as captured:
            with self.assertRaises(NetworkError):
                await request.do_request(url=token_url, method="POST")

        joined = "\n".join(captured.output)
        self.assertNotIn("AAA-secret-token-XYZ", joined)
        self.assertNotIn("7123456789", joined)
        self.assertIn("sendMessage", joined)
