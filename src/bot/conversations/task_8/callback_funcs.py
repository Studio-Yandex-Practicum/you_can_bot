import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import internal_requests.service as api_service
from conversations.task_8.keyboards import (
    CANCEL_LOG_TEXT,
    NEXT_KEYBOARD,
    REPLY_KEYBOARD,
)
from conversations.task_8.templates import (
    TASK_8_CANCELLATION_TEXT,
    TEXT_OF_START_TASK_8,
)
from internal_requests.entities import Answer

_LOGGER = logging.getLogger(__name__)

CHOOSING = 1

CURRENT_TASK = 8
NUMBER_OF_QUESTIONS = 30
FIRST_STAGE = 20
START_QUESTION_NUMBER = 1


async def show_start_of_task_8(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Вывод описания задания 8."""
    query = update.callback_query
    if query is not None:
        await query.message.edit_reply_markup()
    context.user_data["current_question"] = START_QUESTION_NUMBER
    await update.effective_message.reply_text(
        text=TEXT_OF_START_TASK_8,
        reply_markup=NEXT_KEYBOARD,
    )
    return CHOOSING


async def start_question(
    update: Update, _context: ContextTypes.DEFAULT_TYPE, question_number: int = 1
) -> None:
    """Начинает новый вопрос."""
    await update.callback_query.answer()
    messages = await api_service.get_messages_with_question(
        task_number=CURRENT_TASK,
        question_number=question_number,
    )
    await update.effective_message.reply_text(
        text=messages[0].content,
        reply_markup=REPLY_KEYBOARD,
        parse_mode=ParseMode.HTML,
    )


async def update_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик вопросов."""
    picked_choice = update.callback_query.data
    message = update.effective_message
    await message.edit_text(
        text=f"{message.text_html}\n\nОтвет: {picked_choice.upper()}",
        parse_mode=ParseMode.HTML,
    )
    if picked_choice == "а":
        picked_choice = "б"
    else:
        picked_choice = "а"

    current_question = context.user_data.get("current_question")
    await api_service.create_answer(
        Answer(
            telegram_id=message.chat_id,
            task_number=CURRENT_TASK,
            number=current_question,
            content=picked_choice,
        )
    )
    # if current_question == NUMBER_OF_QUESTIONS:
    #     context.user_data.clear()
    #     return await show_result(update, context)
    context.user_data["current_question"] += 1
    await start_question(update, context, context.user_data.get("current_question"))
    return CHOOSING


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Конец диалога."""
    _LOGGER.info(CANCEL_LOG_TEXT, update.effective_chat.id)
    context.user_data.clear()
    await update.effective_message.reply_text(TASK_8_CANCELLATION_TEXT)
    return ConversationHandler.END
