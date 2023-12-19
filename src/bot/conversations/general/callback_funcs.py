import html
import logging
import traceback
from asyncio import sleep
from typing import Optional

from httpx import HTTPStatusError, codes
from telegram import Bot, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import conversations.general.keyboards as keyboards
import conversations.general.templates as templates
import internal_requests.service as api_service
from conversations.general.decorators import not_in_conversation, set_conversation_name
from external_requests import NAME, SURNAME, TARIFF, get_user_info_from_lk
from external_requests.exceptions import APIDataError, PostAPIError, UserNotFound
from internal_requests.entities import UserFromTelegram
from utils.configs import ALLOWED_TARIFFS, DEVELOPER_CHAT_ID

DELAY_TO_AVOID_FLOOD = 5

_LOGGER = logging.getLogger(__name__)

HELLO = 0


@not_in_conversation(ConversationHandler.END)
@set_conversation_name("start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Первое сообщение от бота при вводе команды /start."""
    try:
        user_info = await api_service.get_info_about_user(
            telegram_id=update.effective_chat.id
        )
    except HTTPStatusError as exception:
        if exception.response.status_code != codes.NOT_FOUND:
            raise exception
        user_info_from_lk = await _get_user_info_from_lk_and_handle_it(update)
        if user_info_from_lk is None:
            del context.user_data["current_conversation"]
            return ConversationHandler.END
        if user_info_from_lk[TARIFF] not in ALLOWED_TARIFFS:
            await update.effective_chat.send_message(
                templates.NOT_ALLOWED_TARIFFS_START_MESSAGE.format(
                    name=user_info_from_lk[NAME]
                )
            )
            del context.user_data["current_conversation"]
            return ConversationHandler.END
        user_info = await _save_user_info_to_db(update, user_info_from_lk)

    await update.effective_chat.send_message(
        templates.ALLOWED_TARIFFS_START_MESSAGE.format(name=user_info.name),
        reply_markup=keyboards.HELLO_KEYBOARD,
    )

    return HELLO


async def show_skill_set_info(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Выводит сообщение пользователю о том, зачем ему бот."""
    query = update.callback_query
    await query.answer()
    await update.effective_chat.send_message(
        templates.SKILL_SET_INFORMATION,
        reply_markup=keyboards.FIRST_TASK_KEYBOARD,
    )
    await update.callback_query.edit_message_reply_markup()
    del context.user_data["current_conversation"]
    return ConversationHandler.END


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает ошибку, логирует исключение с информацией из контекста пользователя,
    уведомляет разработчика об ошибке."""
    await _log_exception_with_user_context(context)

    await _notify_developer_of_error(context)

    if isinstance(update, Update):
        await _handle_error_and_clear_context(update, context)


async def _log_exception_with_user_context(context):
    _LOGGER.error(
        "При обработке обновления было вызвано исключение:\n\n"
        f"context.chat_data = {str(context.chat_data)}\n\n"
        f"context.user_data = {str(context.user_data)}\n\n",
        exc_info=context.error,
    )


async def _save_user_info_to_db(update: Update, user_info: dict) -> UserFromTelegram:
    """Отправляет информацию о новом пользователе в backend."""
    telegram_id = update.effective_chat.id
    user_info = UserFromTelegram(
        telegram_id=telegram_id,
        telegram_username=update.effective_user.username,
        name=user_info[NAME],
        surname=user_info[SURNAME],
    )
    await api_service.create_user(user=user_info)
    return user_info


async def _get_user_info_from_lk_and_handle_it(update: Update) -> Optional[dict]:
    """Совершает запрос к ЛК и возвращает полученный словарь, обрабатывает ошибки."""
    try:
        user_info = await get_user_info_from_lk(update.effective_user.id)
        return user_info
    except UserNotFound:
        await update.message.reply_text(templates.UNKNOWN_START_MESSAGE)
    except ConnectionError:
        await update.message.reply_text(templates.CONNECTION_ERROR_MESSAGE)
    except (HTTPStatusError, PostAPIError, APIDataError):
        await update.message.reply_text(templates.SERVER_ERROR_MESSAGE)
    except Exception as error:
        raise error


async def _notify_developer_of_error(context):
    """Уведомляет разработчика об ошибке."""
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)
    message = (
        "При обработке обновления было вызвано исключение:\n"
        f"{html.escape(tb_string)}"
    )
    await _send_long_message(
        message=message, chat_id=DEVELOPER_CHAT_ID, bot_instance=context.bot
    )


async def _handle_error_and_clear_context(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Чистит context пользователя, у которого случилась ошибка."""
    context.user_data.clear()
    await update.effective_message.reply_text(
        "Ой, что-то пошло не так! Попробуй, пожалуйста, позже."
    )


async def _send_long_message(message: str, chat_id: int, bot_instance: Bot) -> None:
    max_message_len = 4096
    if len(message) > max_message_len:
        message_parts = [
            message[i : i + max_message_len]
            for i in range(0, len(message), max_message_len)
        ]
        for part in message_parts:
            await sleep(DELAY_TO_AVOID_FLOOD)
            await bot_instance.send_message(
                chat_id=chat_id,
                text="<pre>" + part + "</pre>",
                parse_mode=ParseMode.HTML,
            )
    else:
        await bot_instance.send_message(
            chat_id=chat_id,
            text="<pre>" + message + "</pre>",
            parse_mode=ParseMode.HTML,
        )
