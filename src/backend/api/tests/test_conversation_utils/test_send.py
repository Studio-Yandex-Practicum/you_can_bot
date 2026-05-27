from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from telegram.error import BadRequest, NetworkError

from api.conversation_utils import (
    SEND_MESSAGE_MAX_ATTEMPTS,
    non_context_send_message,
)


def _make_bot(send_mock):
    """Build a MagicMock that behaves like an async context manager bot."""
    bot = MagicMock()
    bot.__aenter__ = AsyncMock(return_value=bot)
    bot.__aexit__ = AsyncMock(return_value=None)
    bot.send_message = send_mock
    return bot


class NonContextSendMessageTests(IsolatedAsyncioTestCase):
    """Smoke tests for the retry behaviour of non_context_send_message."""

    @patch("api.conversation_utils.asyncio.sleep", new=AsyncMock())
    @patch("api.conversation_utils._build_bot")
    async def test_forwards_parse_mode_on_success(self, build_bot):
        send_mock = AsyncMock()
        build_bot.return_value = _make_bot(send_mock)

        await non_context_send_message("hi", user_id=1, parse_mode="HTML")

        send_mock.assert_awaited_once_with(
            chat_id=1, text="hi", parse_mode="HTML"
        )

    @patch("api.conversation_utils.asyncio.sleep", new=AsyncMock())
    @patch("api.conversation_utils._build_bot")
    async def test_retries_network_error_then_succeeds(self, build_bot):
        send_mock = AsyncMock(side_effect=[NetworkError("flap"), None])
        build_bot.return_value = _make_bot(send_mock)

        await non_context_send_message("hi", user_id=1)

        self.assertEqual(send_mock.await_count, 2)

    @patch("api.conversation_utils.asyncio.sleep", new=AsyncMock())
    @patch("api.conversation_utils._build_bot")
    async def test_reraises_after_max_attempts(self, build_bot):
        send_mock = AsyncMock(side_effect=NetworkError("down"))
        build_bot.return_value = _make_bot(send_mock)

        with self.assertRaises(NetworkError):
            await non_context_send_message("hi", user_id=1)
        self.assertEqual(send_mock.await_count, SEND_MESSAGE_MAX_ATTEMPTS)

    @patch("api.conversation_utils.asyncio.sleep", new=AsyncMock())
    @patch("api.conversation_utils._build_bot")
    async def test_does_not_retry_bad_request(self, build_bot):
        send_mock = AsyncMock(side_effect=BadRequest("Can't parse entities"))
        build_bot.return_value = _make_bot(send_mock)

        with self.assertRaises(BadRequest):
            await non_context_send_message(
                "<bad>", user_id=1, parse_mode="HTML"
            )
        send_mock.assert_awaited_once()
