import re

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import internal_requests.service as api_service
from conversations.task_1.keyboards import (
    GO_TO_TASK_2_KEYBOARD,
    START_TASK_1_KEYBOARD,
    get_inline_keyboard,
)
from conversations.task_1.templates import (
    CANCEL_TEXT,
    END_TASK_1_TEXT,
    SCORES,
    START_TASK_1_TEXT,
)
from internal_requests.entities import Answer

CHOICES = "АБВГДЕ"
CHOOSING = 1
CURRENT_TASK = 1
IDX_IN_STR = 4
MAX_SCORE = 5
NUMBER_OF_QUESTIONS = 10
START_QUESTION_NUMBER = 1
LABEL_PATTERN = r"\[([А-Я])\]"


async def start_task_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выводит описание задания 1."""
    query = update.callback_query
    print(query)
    if query is not None:
        await query.message.edit_reply_markup()
    context.user_data["current_question"] = START_QUESTION_NUMBER
    await update.effective_message.reply_text(
        text=START_TASK_1_TEXT,
        reply_markup=START_TASK_1_KEYBOARD,
    )
    return CHOOSING


async def get_start_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE, question_number: int = 1
) -> None:
    """Начинает новый вопрос."""
    await update.callback_query.answer()
    context.user_data["picked_choices"] = ""
    messages = await api_service.get_messages_with_question(
        task_number=CURRENT_TASK,
        question_number=question_number,
    )
    await update.effective_message.reply_text(
        text=messages[0].content,
        reply_markup=get_inline_keyboard(CHOICES),
        parse_mode=ParseMode.HTML,
    )


async def end_task_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.reply_text(
        text=END_TASK_1_TEXT,
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
        reply_markup=GO_TO_TASK_2_KEYBOARD,
    )
    context.user_data.clear()
    return ConversationHandler.END


async def get_answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопок."""
    choice = update.callback_query.data
    context.user_data["picked_choices"] += choice
    picked_choices = context.user_data.get("picked_choices")
    message = update.effective_message
    await update.effective_message.edit_text(
        _get_question_text(message.text_html.split("\n\n"), picked_choices),
        reply_markup=get_inline_keyboard(CHOICES, picked_choices),
        parse_mode=ParseMode.HTML,
    )

    current_question = context.user_data.get("current_question")
    if len(picked_choices) == len(CHOICES):
        await _save_answer(message.chat_id, current_question, picked_choices)
        if current_question == NUMBER_OF_QUESTIONS:
            state = await end_task_1(update, context)
            return state
        context.user_data["current_question"] += 1
        await get_start_question(
            update, context, context.user_data.get("current_question")
        )
    return CHOOSING


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Прерывает выполнение задания."""
    await update.message.reply_text(CANCEL_TEXT)
    context.user_data.clear()
    return ConversationHandler.END


def _get_question_text(message_text, picked_choices: str = "") -> str:
    text = f"{message_text[0]}\n\n"
    for string in message_text[1:]:
        text += f"{string}"
        if re.search(LABEL_PATTERN, string).group(1) == picked_choices[-1]:
            text += f" — {SCORES[MAX_SCORE - picked_choices.index(string[IDX_IN_STR])]}"
        text += "\n\n"
    return text


async def _save_answer(user_id, current_question, picked_choices):
    """Сохраняет ответ пользователя в БД."""
    answers = ""
    for label in CHOICES:
        answers += str(MAX_SCORE - picked_choices.index(label))
    await api_service.create_answer(
        Answer(
            telegram_id=user_id,
            task_number=CURRENT_TASK,
            number=current_question,
            content=answers,
        )
    )
