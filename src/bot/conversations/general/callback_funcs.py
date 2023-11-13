from httpx import HTTPStatusError, codes
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

import conversations.general.keyboards as keyboards
import conversations.general.templates as templates
import internal_requests.service as api_service
from conversations import CANCEL_ACQUAINTANCE, START_MESSAGE
from external_requests import NAME, SURNAME, TARIFF, get_user_info_from_lk
from external_requests.exceptions import (
    APIDataError,
    APIForbiddenError,
    PostAPIError,
    TelegramIdError,
    UserNotFound,
)
from internal_requests.entities import UserFromTelegram
from utils.configs import ALLOWED_TARIFFS

HELLO = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Первое сообщение от бота при вводе команды /start."""
    await _get_user_info_and_set_in_context(update, context)
    if not context.user_info:
        return ConversationHandler.END
    if context.user_info[TARIFF] not in ALLOWED_TARIFFS:
        await update.effective_chat.send_message(
            templates.NOT_ALLOWED_TARIFFS_START_MESSAGE.format(
                name=context.user_info[NAME]
            )
        )
        return ConversationHandler.END

    await _get_or_create_user_from_telegram(update, context)
    await update.effective_chat.send_message(
        templates.ALLOWED_TARIFFS_START_MESSAGE.format(name=context.user_info[NAME]),
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
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершает диалог с пользователем."""
    query = update.callback_query
    await query.answer(CANCEL_ACQUAINTANCE)
    await query.edit_message_text(START_MESSAGE)
    context.user_data.clear()
    return ConversationHandler.END


async def _get_or_create_user_from_telegram(update, context):
    """Получает информацию о пользователе по telegram_id.
    При отсутствии создаёт новый экземпляр UserFromTelegram.
    """
    telegram_id = update.effective_user.id
    try:
        user = await api_service.get_info_about_user(telegram_id)
    except HTTPStatusError as exception:
        if exception.response.status_code != codes.NOT_FOUND:
            raise exception
        user = UserFromTelegram(
            telegram_id=telegram_id,
            telegram_username=update.effective_user.username,
            name=context.user_info[NAME],
            surname=context.user_info[SURNAME],
        )
        await api_service.create_user(user)
    return user


async def _get_user_info_and_set_in_context(update, context):
    """Добавляет информацию о пользователе в context."""
    context.user_info = None
    try:
        context.user_info = await get_user_info_from_lk(update.effective_user.id)
    except UserNotFound:
        await update.message.reply_text(templates.UNKNOWN_START_MESSAGE)
    except APIDataError:
        await update.message.reply_text(templates.DATA_ERROR_MESSAGE)
    except (APIForbiddenError, TelegramIdError):
        await update.message.reply_text(templates.INTERNAL_ERROR_MESSAGE)
    except ConnectionError:
        await update.message.reply_text(templates.CONNECTION_ERROR_MESSAGE)
    except (HTTPStatusError, PostAPIError):
        await update.message.reply_text(templates.SERVER_ERROR_MESSAGE)
    except Exception as e:
        print(str(e))
        await update.message.reply_text(templates.INTERNAL_ERROR_MESSAGE)
        raise Exception
