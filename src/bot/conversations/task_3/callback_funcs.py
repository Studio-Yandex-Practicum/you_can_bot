import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import internal_requests.service as api_service
from conversations.task_3.keyboards import (
    ANSWER,
    CANCEL_KEYBOARD,
    CANSEL,
    NEXT_KEYBOARD,
    REPLY_KEYBOARD,
)
from conversations.task_3.templates import (
    RESULT_MESSAGE,
    TASK_3_CANCELLATION_TEXT,
    TEXT_OF_START_TASK_3,
)
from internal_requests.entities import Answer

_LOGGER = logging.getLogger(__name__)
ANSWER_ERROR = (
    "Ошибка при обращении к вопросу №{number}:/n Url: {url}/n Ошибка: {error}."
)

DESCRIPTION_MARKER = "Последний вопрос"
FIRST_QUESTION_MARKER = "Первый вопрос"
OTHER_QUESTIONS_MARKER = "Следующий вопрос"

CURRENT_TASK = 3
NUMBER_OF_QUESTIONS = 42
START_QUESTION_NUMBER = 1


async def show_start_of_task_3(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Выводит описание задания 3."""
    context.user_data["current_question"] = START_QUESTION_NUMBER
    await update.effective_message.reply_text(
        text=TEXT_OF_START_TASK_3,
        reply_markup=NEXT_KEYBOARD,
    )
    return FIRST_QUESTION_MARKER


async def show_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> str:
    """Обработчик вопросов."""
    await update.callback_query.answer()
    current_question = context.user_data.get("current_question")
    if current_question != START_QUESTION_NUMBER:
        _LOGGER.info(
            ANSWER,
            update.effective_message.from_user.username,
            current_question - START_QUESTION_NUMBER,
            update.effective_message.text,
        )
    messages = await api_service.get_messages_with_question(
        task_number=CURRENT_TASK,
        question_number=current_question,
    )
    try:
        # Здесь должна выводиться картинка - еще не реализовано
        # await context.bot.send_photo(
        #     chat_id=update.effective_chat.id,
        #     photo=messages[0].photo,
        #     disable_notification=True,
        # )

        await update.effective_message.reply_text(
            text=messages[0].content,
            reply_markup=REPLY_KEYBOARD,
            parse_mode=ParseMode.HTML,
        )
        if current_question != START_QUESTION_NUMBER:
            await api_service.create_answer(
                Answer(
                    telegram_id=update.effective_message.chat_id,
                    task_number=CURRENT_TASK,
                    number=current_question,
                    content=update.callback_query.data,
                )
            )
            print(update.callback_query.data)

    except ConnectionError as error:
        _LOGGER.error(
            ANSWER_ERROR.format(
                number=current_question, url=messages[0].photo, error=error
            )
        )
    if current_question == NUMBER_OF_QUESTIONS:
        context.user_data.clear()
        return DESCRIPTION_MARKER
    current_question += 1
    context.user_data["current_question"] = current_question
    return OTHER_QUESTIONS_MARKER


async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Расшифровка."""
    _LOGGER.info(
        ANSWER,
        update.effective_message.from_user.username,
        NUMBER_OF_QUESTIONS,
        update.effective_message.text,
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=RESULT_MESSAGE
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Конец диалога."""
    _LOGGER.info(CANSEL, update.effective_message.from_user.first_name)
    context.user_data.clear()
    await update.effective_message.reply_text(
        TASK_3_CANCELLATION_TEXT, reply_markup=CANCEL_KEYBOARD
    )
    return ConversationHandler.END
