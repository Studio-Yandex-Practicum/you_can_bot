from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from internal_requests.service import get_info_about_user


def user_exists(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        try:
            await get_info_about_user(telegram_id)
            return await func(update, context)
        except Exception as e:
            print(f"Ошибка c пользователем: {e}")
            return ConversationHandler.END

    return wrapper
