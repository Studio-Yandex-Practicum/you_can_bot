import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import internal_requests.service as api_service
from conversations.task_3.keyboards import (
    CANCEL_KEYBOARD,
    CANSEL,
    GO_TO_TASK_4_KEYBOARD,
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

CHOOSING = 1
CURRENT_TASK = 3
NUMBER_OF_QUESTIONS = 42
START_QUESTION_NUMBER = 1


async def show_start_of_task_3(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Выводит описание задания 3."""
    context.user_data.clear()
    context.user_data["current_question"] = START_QUESTION_NUMBER
    await update.effective_message.reply_text(
        text=TEXT_OF_START_TASK_3,
        reply_markup=NEXT_KEYBOARD,
    )
    return CHOOSING


async def start_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE, question_number: int = 1
) -> None:
    """Начинает новый вопрос."""
    await update.callback_query.answer()
    messages = await api_service.get_messages_with_question(
        task_number=CURRENT_TASK,
        question_number=question_number,
    )
    try:
        # Здесь должна выводиться картинка - еще не реализовано.
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
    except ConnectionError as error:
        _LOGGER.error(
            ANSWER_ERROR.format(
                number=question_number, url=messages[0].photo, error=error
            )
        )


async def update_question(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> str:
    """Обработчик вопросов."""
    picked_choice = update.callback_query.data
    message = update.effective_message
    await message.edit_text(
        text=(f"{message.text_html}\n\n" f"Ответ: {picked_choice.upper()}"),
        parse_mode=ParseMode.HTML,
    )

    current_question = context.user_data.get("current_question")
    await api_service.create_answer(
        Answer(
            telegram_id=message.chat_id,
            task_number=CURRENT_TASK,
            number=current_question,
            content=update.callback_query.data,
        )
    )
    if current_question == NUMBER_OF_QUESTIONS:
        context.user_data.clear()
        return await show_result(update, context)
    context.user_data["current_question"] += 1
    await start_question(update, context, context.user_data.get("current_question"))
    return CHOOSING


async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Расшифровка."""
    query = update.callback_query
    await query.message.reply_text(
        text=RESULT_MESSAGE,
        parse_mode=ParseMode.HTML,
    )
    results = await api_service.get_messages_with_results(
        telegram_id=query.from_user.id, task_number=CURRENT_TASK
    )
    for result in results[:-1]:
        await query.message.reply_text(
            text=result.content,
            parse_mode=ParseMode.HTML,
        )
    await query.message.reply_text(
        text=results[-1].content,
        parse_mode=ParseMode.HTML,
        reply_markup=GO_TO_TASK_4_KEYBOARD,
    )
    context.user_data.clear()
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Конец диалога."""
    _LOGGER.info(CANSEL, update.effective_message.from_user.first_name)
    context.user_data.clear()
    await update.effective_message.reply_text(
        TASK_3_CANCELLATION_TEXT, reply_markup=CANCEL_KEYBOARD
    )
    return ConversationHandler.END
