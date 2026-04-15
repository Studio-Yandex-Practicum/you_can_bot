from django.conf import settings
from telegram import Bot
from telegram.request import HTTPXRequest


def _build_bot():
    kwargs = {"token": settings.TOKEN}
    if settings.SOCKS5_PROXY_URL:
        kwargs["request"] = HTTPXRequest(proxy=settings.SOCKS5_PROXY_URL)
    return Bot(**kwargs)


async def non_context_send_message(text, user_id):
    """
    Отправляет сообщение пользователю без update и context.
    Отправляет сообщение куратору, когда задание выполнено студентом.
    """
    async with _build_bot() as bot:
        await bot.send_message(chat_id=user_id, text=text)
