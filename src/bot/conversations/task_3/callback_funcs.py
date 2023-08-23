import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from conversations.task_3.keyboards import (
    ANSWER,
    CANSEL,
    INPUT_PLACEHOLDER,
    NEXT_KEYBOARD,
    NEXT_PLACEHOLDER,
    REPLY_KEYBOARD
)
from conversations.task_3.templates import (
    DELIMETER_TEXT_FROM_URL,
    QUESTIONS,
    RESULT_MESSAGE,
    TASK_3_CANCELLATION_TEXT,
    TEXT_OF_START_OF_TASK_3
)


FIRST_QUESTION_MARKER = "Первый вопрос"
OTHER_QUESTIONS_MARKER = "Следующий вопрос"
DESCRIPTION_MARKER = "Последний вопрос"
LAST_MESSAGE = len(QUESTIONS) - 1
ANSWER_ERROR = (
    "Ошибка при обращении к вопросу №{number}:/n Url: {url}/n Ошибка: {error}."
)
_LOGGER = logging.getLogger(__name__)


async def show_start_of_test_3(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Вступление."""
    await update.message.reply_text(
        TEXT_OF_START_OF_TASK_3,
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
            update.message.text,
        )
    parsed_answer = QUESTIONS[current_question].split(DELIMETER_TEXT_FROM_URL)
    try:
        await update.message.reply_text(
            f"{current_question + 1}. {parsed_answer[0]}",
            reply_markup=ReplyKeyboardMarkup(
                REPLY_KEYBOARD,
                one_time_keyboard=True,
                resize_keyboard=True,
                input_field_placeholder=INPUT_PLACEHOLDER,
            )
        )
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=parsed_answer[1],
            disable_notification=True
        )
    except ConnectionError as error:
        _LOGGER.error(
            ANSWER_ERROR.format(
                number=current_question, url=parsed_answer[1], error=error
            )
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
        ANSWER, update.message.from_user.username, LAST_MESSAGE, update.message.text
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
        TASK_3_CANCELLATION_TEXT, reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
