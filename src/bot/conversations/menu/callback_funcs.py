from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

import conversations.menu.templates as templates
import internal_requests.service as api_service
from conversations.general.decorators import not_in_conversation, set_conversation_name
from conversations.general.logging_decorators import log_decorator
from conversations.menu.cancel_command.callback_funcs import _LOGGER
from conversations.menu.decorators import user_exists
from conversations.menu.keyboards import (
    AGREE_OR_CANCEL_KEYBOARD,
    INFO_URL_KEYBOARD,
    create_inline_tasks_keyboard,
)
from conversations.tasks.base import PICKED_TASK_TEXT
from internal_requests.entities import Problem
from utils.error_handler import error_decorator


@error_decorator(logger=_LOGGER)
async def show_done_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    task_number = int(query.data.split("_")[-1])

    await update.effective_message.edit_reply_markup()
    task_info = await api_service.get_task_info_by_number(task_number=task_number)
    await update.effective_chat.send_message(
        text=PICKED_TASK_TEXT.format(
            task_number=task_info.number, task_name=task_info.name
        ),
    )

    task_results = await api_service.get_messages_with_results(
        update.effective_chat.id, task_number
    )
    for result in task_results:
        await update.effective_message.reply_text(text=result.content)

    del context.user_data["current_conversation"]

    return ConversationHandler.END


@user_exists
@not_in_conversation
@log_decorator(_LOGGER)
@set_conversation_name("tasks")
@error_decorator(_LOGGER)
async def show_all_user_tasks(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Посмотреть список заданий."""
    tasks = await api_service.get_user_task_status_list(
        telegram_id=update.effective_user.id
    )
    keyboard = create_inline_tasks_keyboard(tasks)
    await update.effective_chat.send_message(
        text=templates.TASKS_LIST_TEXT,
        reply_markup=keyboard,
    )
    return templates.TASKS_STATE


@user_exists
@not_in_conversation
@log_decorator(_LOGGER)
@set_conversation_name("ask")
@error_decorator(_LOGGER)
async def suggest_ask_question(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Задать вопрос специалисту."""
    await update.message.reply_text(templates.ASK_ME_QUESTION_TEXT)
    return templates.WAITING_FOR_QUESTION_STATE


@error_decorator(logger=_LOGGER)
async def handle_user_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Принимает текстовый вопрос от пользователя и просит его подтвердить."""
    question_text = update.message.text
    question_id = update.message.message_id
    if question_text and question_id:
        context.user_data["question"] = question_text
        context.user_data["question_id"] = question_id
        confirmation_message = await update.message.reply_text(
            text=templates.SEND_QUESTION_TEXT + '"' + question_text + '"',
            reply_markup=AGREE_OR_CANCEL_KEYBOARD,
        )
        context.user_data["confirmation_message_id"] = confirmation_message.message_id
        return templates.WAITING_FOR_CONFIRMATION_STATE
    return templates.WAITING_FOR_QUESTION_STATE


@error_decorator(logger=_LOGGER)
async def handle_user_question_edit(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """
    Принимает измененный текстовый вопрос от пользователя и просит его подтвердить.
    """
    original_question_id = context.user_data.get("question_id")
    confirmation_message_id = context.user_data.get("confirmation_message_id")
    if (
        update.edited_message.message_id == original_question_id
        and confirmation_message_id
    ):
        question_text = update.edited_message.text
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=confirmation_message_id,
            text=templates.SEND_QUESTION_TEXT + '"' + question_text + '"',
            reply_markup=AGREE_OR_CANCEL_KEYBOARD,
        )
        context.user_data["question"] = question_text
    return templates.WAITING_FOR_CONFIRMATION_STATE


@error_decorator(logger=_LOGGER)
async def confirm_saving_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Сохраняет вопрос в базу данных."""
    question = context.user_data["question"]
    problem = Problem(telegram_id=update.effective_user.id, message=question)
    await api_service.create_question_from_user(problem)
    context.user_data.clear()
    await update.effective_message.edit_text(text=templates.QUESTION_CONFIRMATION_TEXT)
    return ConversationHandler.END


@error_decorator(logger=_LOGGER)
async def cancel_save_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отменяет отправку вопроса."""
    context.user_data.clear()
    await update.effective_message.edit_text(text=templates.QUESTION_CANCEL)
    return ConversationHandler.END


@not_in_conversation
@log_decorator(_LOGGER)
@error_decorator(logger=_LOGGER)
async def show_info_url(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Перейти на сайт YouCan."""
    await update.message.reply_text(
        text=templates.GET_MORE_INFO_TEXT,
        reply_markup=INFO_URL_KEYBOARD,
    )
