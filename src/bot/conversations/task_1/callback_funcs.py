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
    RESULT,
    SCORES,
    START_TASK_1_TEXT,
)
from internal_requests.entities import Answer

CHOICES = "АБВГДЕ"
CHOOSING = 1
CURRENT_TASK = 1
MAX_SCORE = 5
NUMBER_OF_QUESTIONS = 10
START_QUESTION_NUMBER = 1


async def start_task_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выводит описание задания 1."""
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
    context.user_data["picked_choices"] = ""
    messages = await api_service.get_messages_with_question(
        task_number=CURRENT_TASK,
        question_number=question_number,
    )
    await update.effective_message.reply_text(
        text=messages[0].content,
        reply_markup=get_inline_keyboard(
            CHOICES,
        ),
        parse_mode=ParseMode.HTML,
    )


async def end_task_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.reply_text(
        text=END_TASK_1_TEXT,
        reply_markup=GO_TO_TASK_2_KEYBOARD,
    )
    for result in _get_result(query.from_user, context):
        await query.message.reply_text(
            text=RESULT[result],
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    return ConversationHandler.END


async def get_answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопок."""

    choice = update.callback_query.data
    context.user_data["picked_choices"] += choice
    picked_choices = context.user_data.get("picked_choices")
    message = update.effective_message
    print(message, picked_choices)
    await update.effective_message.edit_text(
        _get_question_text(message.text.split("\n\n"), picked_choices),
        reply_markup=get_inline_keyboard(CHOICES, picked_choices),
        parse_mode=ParseMode.HTML,
    )

    current_question = context.user_data.get("current_question")
    if len(picked_choices) == len(CHOICES):
        _save_answer(message.from_user.id, current_question, picked_choices)
        if current_question == NUMBER_OF_QUESTIONS:
            await end_task_1(update, context)
        context.user_data["current_question"] += 1
        await get_start_question(
            update, context, context.user_data.get("current_question")
        )
    return CHOOSING


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Прерывает выполнение задания."""
    await update.message.reply_text(CANCEL_TEXT)
    return ConversationHandler.END


def _get_question_text(message_text, picked_choices: str = "") -> str:
    text = f"{message_text[0]}\n"
    for string in message_text[1:]:
        text += f"{string}"
        if string[1] in picked_choices:
            text += f" — {SCORES[MAX_SCORE - picked_choices.index(string[1])]}"
        text += "\n"
    return text


async def _save_answer(user_id, current_question, picked_choices):
    """Сохраняет ответ пользователя в БД."""
    answers = ""
    for lable in CHOICES:
        answers += MAX_SCORE - picked_choices.index(lable)
    await api_service.create_answer(
        Answer(
            telegram_id=user_id,
            task_number=CURRENT_TASK,
            number=current_question,
            content=answers,
        )
    )


def _get_result(user, context):  # Временная, расшифровывает из контекста
    """Получает расшифровку"""
    result = {"1": None, "2": None, "3": None}
    for choice, score in context.user_data["answer"].items():
        if result["1"] is None or result["1"][0] < score:
            result["3"] = result["2"]
            result["2"] = result["1"]
            result["1"] = (score, choice)
        elif result["2"] is None or result["2"][0] < score:
            result["3"] = result["2"]
            result["2"] = (score, choice)
        elif result["3"] is None or result["3"][0] < score:
            result["3"] = (score, choice)
        else:
            pass
    return result["1"][1], result["2"][1], result["3"][1]
