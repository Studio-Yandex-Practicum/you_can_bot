import logging
from typing import Optional

from httpx import HTTPStatusError, codes
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

import conversations.general.keyboards as keyboards
import conversations.general.templates as templates
import internal_requests.service as api_service
from conversations.general.decorators import not_in_conversation, set_conversation_name
from conversations.general.logging_decorators import log_decorator
from external_requests import get_user_info_from_lk
from external_requests.exceptions import UserNotFound
from external_requests.service import FIRST_NAME, LAST_NAME, TARIFF, UserInfo
from internal_requests.entities import UserFromTelegram
from utils.configs import ALLOWED_TARIFFS
from utils.error_handler import error_decorator

_LOGGER = logging.getLogger(__name__)

HELLO = 0


@not_in_conversation
@log_decorator(_LOGGER)
@error_decorator(_LOGGER)
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
                    name=user_info_from_lk[FIRST_NAME]
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


async def _save_user_info_to_db(update: Update, user_info: dict) -> UserFromTelegram:
    """Отправляет информацию о новом пользователе в backend."""
    telegram_id = update.effective_chat.id
    user_info = UserFromTelegram(
        telegram_id=telegram_id,
        telegram_username=update.effective_user.username,
        name=user_info[FIRST_NAME],
        surname=user_info[LAST_NAME],
    )
    await api_service.create_user(user=user_info)
    return user_info


async def _get_user_info_from_lk_and_handle_it(update: Update) -> Optional[UserInfo]:
    """Совершает запрос к ЛК и возвращает полученный словарь, обрабатывает ошибки."""
    try:
        user_info = await get_user_info_from_lk(update.effective_user.id)
        return user_info
    except UserNotFound:
        await update.message.reply_text(templates.UNKNOWN_START_MESSAGE)
    except Exception as error:
        raise error
