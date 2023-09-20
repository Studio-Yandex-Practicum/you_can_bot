import re

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler
import internal_requests.service as api_service

from conversations.task_1.keyboards import get_inline_keyboard, get_reply_keyboard
from conversations.task_1.templates import MESSAGES, RESULT, SCORE

INITIAL_MESSAGE_NUMBER = 5
CHOICES = "АБВГДЕ"
MESSAGE_KEY_TEMPLATE = "message_{}"
NUMBER_OF_QUESTIONS = 10
CHOOSING = 1
CANCEL_TEXT = "Выполнение задания 1 было пропущено"
CURRENT_TASK = 1


async def start_task_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начальное соостояние задания."""
    context.user_data["answer"] = {
        "А": 0,
        "Б": 0,
        "В": 0,
        "Г": 0,
        "Д": 0,
        "Е": 0,
    }  # временное хранение ответа
    template = _get_question_template(context, start=True)
    await update.message.reply_text(
        template["text"],
        reply_markup=get_reply_keyboard(template["buttons"]),
    )
    return CHOOSING


async def question_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE, question_number: int = 1
) -> None:
    """Начинает новый вопрос."""
    context.user_data["current_question"] = question_number
    context.user_data["picked_choices"] = ""
    template = _get_question_template(context)
    if update.message:
        await update.message.reply_text(
            _get_question_text(template),
            reply_markup=get_inline_keyboard(
                template["buttons"],
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    else:
        await update.callback_query.message.reply_text(
            _get_question_text(template),
            reply_markup=get_inline_keyboard(
                template["buttons"],
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопок."""
    if update.message:
        await question_start(update, context)
    else:
        choice = update.callback_query.data
        context.user_data["picked_choices"] += choice
        template = _get_question_template(context)
        await update.callback_query.edit_message_text(
            _get_question_text(template, context.user_data.get("picked_choices")),
            reply_markup=get_inline_keyboard(
                template["buttons"], context.user_data.get("picked_choices")
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    if len(context.user_data.get("picked_choices")) == len(CHOICES):
        _save_answer(update.callback_query.from_user, context)
        if context.user_data.get("current_question") == NUMBER_OF_QUESTIONS:
            query = update.callback_query
            template = _get_question_template(context, result=True)
            await query.message.reply_text(
                f'*{template["text"]}*',
                reply_markup=get_reply_keyboard(
                    template["buttons"],
                ),
                parse_mode=ParseMode.MARKDOWN_V2,
            )
            results = await api_service.get_messages_with_results(
                telegram_id=query.from_user.id,
                task_number=CURRENT_TASK
            )
            for result in results:
                await query.message.reply_text(
                    text=result.content,
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
            return ConversationHandler.END
        else:
            await question_start(
                update, context, context.user_data.get("current_question") + 1
            )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Прерывает выполнение задания."""
    await update.message.reply_text(CANCEL_TEXT)
    return ConversationHandler.END


def _get_question_template(
    context: ContextTypes.DEFAULT_TYPE,
    start: bool = False,
    result: bool = False,
) -> dict:
    if start:
        message_number = INITIAL_MESSAGE_NUMBER
    elif result:
        message_number = INITIAL_MESSAGE_NUMBER + NUMBER_OF_QUESTIONS + 1
    else:
        message_number = INITIAL_MESSAGE_NUMBER + context.user_data["current_question"]
    return MESSAGES[MESSAGE_KEY_TEMPLATE.format(message_number)]


def _get_question_text(template: dict, picked_choices: str = "") -> str:
    text = f'*{re.escape(template["text"])}*\n'
    for label, choice in template["buttons"].items():
        text += f"*\[{label}\]* {re.escape(choice)}"  # noqa
        if label in picked_choices:
            text += SCORE[len(CHOICES) - picked_choices.index(label) - 1]
        text += "\n"
    return text


def _save_answer(user, context):  # Временная, хранит ответы в контексте
    """Сохраняет ответ пользователя."""
    choices = context.user_data.get("picked_choices")
    for choice in CHOICES:
        context.user_data["answer"][choice] += len(CHOICES) - choices.index(choice) - 1
