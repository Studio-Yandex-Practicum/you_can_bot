import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from conversations.task_4.keyboards import (
    ANSWER,
    BUTTONS,
    CANSEL,
    INPUT_PLACEHOLDER,
    KEYBOARD,
    NEXT_KEYBOARD,
    NEXT_PLACEHOLDER,
)
from conversations.task_4.templates import (
    QUESTIONS,
    RESULT_MESSAGE,
    TASK_4_CANCELLATION_TEXT,
    TEXT_OF_START_OF_TASK_4,
)


FIRST_QUESTION_MARKER = "Первый вопрос"
OTHER_QUESTIONS_MARKER = "Следующий вопрос"
DESCRIPTION_MARKER = "Последний вопрос"
LAST_MESSAGE = len(QUESTIONS) - 1

_LOGGER = logging.getLogger(__name__)


async def show_start_of_test_4(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Вступление."""
    await update.message.reply_text(
        TEXT_OF_START_OF_TASK_4,
        reply_markup=ReplyKeyboardMarkup(
            NEXT_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=NEXT_PLACEHOLDER,
        ),
    )
    return FIRST_QUESTION_MARKER


async def show_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> str:
    """Обработчик вопросов."""
    current_question = context.user_data.get("current_question", 0)
    if current_question != 0:
        _LOGGER.info(
            ANSWER,
            update.message.from_user.username,
            current_question - 1,
            *[
                key for key, value in BUTTONS.items()
                if value == update.message.text
            ],
        )
    await update.message.reply_text(
        f"{current_question + 1}. {QUESTIONS[current_question]}",
        reply_markup=KEYBOARD,
    )
    if current_question == LAST_MESSAGE:
        context.user_data.clear()
        return DESCRIPTION_MARKER
    current_question += 1
    context.user_data["current_question"] = current_question
    return OTHER_QUESTIONS_MARKER


async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Расшифровка."""
    _LOGGER.info(
        ANSWER, update.message.from_user.username, LAST_MESSAGE,
        *[
            key for key, value in BUTTONS.items()
            if value == update.message.text
        ],
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=RESULT_MESSAGE
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Конец диалога."""
    _LOGGER.info(CANSEL, update.message.from_user.first_name)
    context.user_data.clear()
    await update.message.reply_text(
        TASK_4_CANCELLATION_TEXT, reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
