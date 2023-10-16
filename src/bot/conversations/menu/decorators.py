from internal_requests.service import get_info_about_user
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    CallbackContext
)


def user_exists(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        try:
            await get_info_about_user(telegram_id)
            print(t, '-----------------------')
            return await func(update, context)
        except Exception as e:
            print(f'Ошибка: {e}')
            return ConversationHandler.END
    return wrapper
