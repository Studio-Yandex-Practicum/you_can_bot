from httpx import HTTPStatusError, codes
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

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
from internal_requests.service import create_user, get_info_about_user
from utils.configs import ALLOWED_TARIFFS

from .keyboards import FIRST_TASK_KEYBOARD, HELLO_KEYBOARD, START_SKILL_SETS_KEYBOARD
from .templates import (
    ALLOWED_TARIFFS_START_MESSAGE,
    CONNECTION_ERROR_MESSAGE,
    DATA_ERROR_MESSAGE,
    FIRST_SKILL_SET_INFORMATION,
    INTERNAL_ERROR_MESSAGE,
    NOT_ALLOWED_TARIFFS_START_MESSAGE,
    SERVER_ERROR_MESSAGE,
    SKILL_SET_INFORMATION,
    UNKNOWN_START_MESSAGE,
)

HELLO = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Первое сообщение от бота при вводе команды /start."""
    await _get_user_info_and_set_in_context(update, context)
    if not context.user_info:
        return ConversationHandler.END
    if context.user_info[TARIFF] not in ALLOWED_TARIFFS:
        await update.message.reply_text(
            NOT_ALLOWED_TARIFFS_START_MESSAGE.format(name=context.user_info[NAME])
        )
        return ConversationHandler.END

    await _get_or_create_user_from_telegram(update, context)
    await update.message.reply_text(
            ALLOWED_TARIFFS_START_MESSAGE.format(name=context.user_info[NAME]),
            reply_markup=HELLO_KEYBOARD
        )

    return HELLO


async def start_acquaintance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Знакомит пользователя со скиллсетами."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        SKILL_SET_INFORMATION, reply_markup=START_SKILL_SETS_KEYBOARD
    )
    return HELLO


async def start_skill_sets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выдает краткое описание первого задания
    и предлагает к нему приступить."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        FIRST_SKILL_SET_INFORMATION, reply_markup=FIRST_TASK_KEYBOARD
    )
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
        user = await get_info_about_user(telegram_id)
    except HTTPStatusError as exception:
        if exception.response.status_code != codes.NOT_FOUND:
            raise exception
        user = UserFromTelegram(
            telegram_id=telegram_id,
            telegram_username=update.effective_user.username,
            name=context.user_info[NAME],
            surname=context.user_info[SURNAME]
        )
        await create_user(user)
    return user


async def _get_user_info_and_set_in_context(update, context):
    """Добавляет информацию о пользователе в context."""
    context.user_info = None
    try:
        context.user_info = await get_user_info_from_lk(update.effective_user.id)
    except UserNotFound:
        await update.message.reply_text(UNKNOWN_START_MESSAGE)
    except APIDataError:
        await update.message.reply_text(DATA_ERROR_MESSAGE)
    except (APIForbiddenError, TelegramIdError):
        await update.message.reply_text(INTERNAL_ERROR_MESSAGE)
    except ConnectionError:
        await update.message.reply_text(CONNECTION_ERROR_MESSAGE)
    except (HTTPStatusError, PostAPIError):
        await update.message.reply_text(SERVER_ERROR_MESSAGE)
    except Exception:
        await update.message.reply_text(INTERNAL_ERROR_MESSAGE)
