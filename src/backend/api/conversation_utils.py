import os

from telegram import Bot
from telegram.constants import ParseMode

TOKEN = os.getenv("TOKEN")


async def non_context_send_message(text, user_id):
    """
    Отправляет сообщение пользователю без update и context.
    Отправляет сообщение куратору, когда задание выполнено студентом.
    """
    async with Bot(token=TOKEN) as bot:
        await bot.send_message(chat_id=user_id, text=text, parse_mode=ParseMode.HTML)
