import os

from telegram import Bot
from telegram.request import HTTPXRequest

TOKEN = os.getenv("TOKEN")
SOCKS5_PROXY_URL = os.getenv("SOCKS5_PROXY_URL")


def _build_bot():
    kwargs = {"token": TOKEN}
    if SOCKS5_PROXY_URL:
        kwargs["request"] = HTTPXRequest(proxy=SOCKS5_PROXY_URL)
    return Bot(**kwargs)


async def non_context_send_message(text, user_id):
    """
    Отправляет сообщение пользователю без update и context.
    Отправляет сообщение куратору, когда задание выполнено студентом.
    """
    async with _build_bot() as bot:
        await bot.send_message(chat_id=user_id, text=text)
