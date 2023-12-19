from httpx import HTTPStatusError, codes
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from internal_requests.service import get_info_about_user

from .templates import USER_NOT_FOUND


def user_exists(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        try:
            await get_info_about_user(telegram_id)
            return await func(update, context)
        except HTTPStatusError as exception:
            if exception.response.status_code == codes.NOT_FOUND:
                await update.message.reply_text(
                    text=USER_NOT_FOUND, parse_mode=ParseMode.HTML
                )
            return ConversationHandler.END

    return wrapper
