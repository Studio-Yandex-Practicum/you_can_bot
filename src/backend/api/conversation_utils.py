import asyncio
import logging

from django.conf import settings
from telegram import Bot
from telegram.error import NetworkError
from telegram.request import HTTPXRequest

logger = logging.getLogger(__name__)

SEND_MESSAGE_MAX_ATTEMPTS = 3
SEND_MESSAGE_INITIAL_DELAY_SECONDS = 1.0


async def non_context_send_message(text, user_id, parse_mode=None):
    """
    Отправляет сообщение пользователю без update и context.
    Отправляет сообщение куратору, когда задание выполнено студентом.
    """
    await _send_with_retry(text, user_id, parse_mode)


async def _send_with_retry(text, user_id, parse_mode):
    delay = SEND_MESSAGE_INITIAL_DELAY_SECONDS
    for attempt in range(1, SEND_MESSAGE_MAX_ATTEMPTS + 1):
        try:
            async with _build_bot() as bot:
                await bot.send_message(
                    chat_id=user_id, text=text, parse_mode=parse_mode
                )
            return
        except NetworkError:
            if attempt == SEND_MESSAGE_MAX_ATTEMPTS:
                logger.exception(
                    "Failed to send message to user %s after %d attempts",
                    user_id,
                    SEND_MESSAGE_MAX_ATTEMPTS,
                )
                raise
            logger.warning(
                "Network error sending message to user %s "
                "(attempt %d/%d), retrying in %.1fs",
                user_id,
                attempt,
                SEND_MESSAGE_MAX_ATTEMPTS,
                delay,
            )
            await asyncio.sleep(delay)
            delay *= 2


def _build_bot():
    kwargs = {"token": settings.TOKEN}
    if settings.SOCKS5_PROXY_URL:
        kwargs["request"] = HTTPXRequest(proxy=settings.SOCKS5_PROXY_URL)
    return Bot(**kwargs)
