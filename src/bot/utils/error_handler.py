from functools import wraps
from logging import Logger

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler


async def handle_error(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    exception: Exception,
    logger: Logger,
) -> int:
    """Обрабатывает непредвиденное исключение внутри ConversationHandler."""
    await _send_user_error_message(update)
    await _log_update_exception(context, exception, logger)
    context.user_data.clear()
    return ConversationHandler.END


def error_decorator(logger):
    def decorator(func):
        @wraps(func)
        async def wrapper(conv_instance, update, context, *args, **kwargs):
            try:
                return await func(conv_instance, update, context, *args, **kwargs)
            except Exception as exception:
                return await handle_error(update, context, exception, logger)

        return wrapper

    return decorator


async def _send_user_error_message(update):
    await update.effective_chat.send_message(
        "Ой, что-то пошло не так! Попробуй, пожалуйста, позже.",
        parse_mode=ParseMode.HTML,
    )


async def _log_update_exception(context, exception, logger):
    logger.error(
        f"Exception while handling an update:\n"
        f"context.chat_data = {context.chat_data}\n"
        f"context.user_data = {context.user_data}",
        exc_info=exception,
    )
