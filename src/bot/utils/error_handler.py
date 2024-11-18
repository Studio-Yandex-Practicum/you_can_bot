from functools import wraps
from logging import Logger
from typing import Optional

from httpx import HTTPStatusError
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes, ConversationHandler

from external_requests.exceptions import ValidationExternalResponseError


async def handle_error(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    exception: Exception,
    logger: Logger,
) -> Optional[int]:
    """Обрабатывает непредвиденное исключение внутри ConversationHandler."""
    if isinstance(exception, ValidationExternalResponseError):
        await _send_user_error_message(
            update,
            msg=(
                "Данные из личного кабинета оказались некорректными."
                " Пожалуйста, попробуй ещё раз позже."
            ),
        )
    else:
        await _send_user_error_message(update)
    await _log_update_exception(context, exception, logger)
    if isinstance(exception, BadRequest):
        return None
    context.user_data.clear()
    return ConversationHandler.END


def error_decorator(logger):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args):
            try:
                return await func(*args)
            except Exception as exception:
                if len(args) == 3:
                    conv_instance, update, context = args
                else:
                    update, context = args
                return await handle_error(update, context, exception, logger)

        return wrapper

    return decorator


async def _send_user_error_message(
    update, msg="Ой, что-то пошло не так! Попробуй, пожалуйста, позже."
):
    await update.effective_chat.send_message(
        msg,
    )


async def _log_update_exception(context, exception, logger):
    message = (
        f"Exception while handling an update:\n"
        f"context.chat_data = {context.chat_data}\n"
        f"context.user_data = {context.user_data}"
    )
    if isinstance(exception, HTTPStatusError):
        message += "\nresponse = "
        message += exception.response.text
    logger.error(
        message,
        exc_info=exception,
    )
