import logging
from typing import Callable, Optional

from telegram import Update
from telegram.ext import CallbackContext, ContextTypes, ConversationHandler

import conversations.menu.templates as templates
import internal_requests.service as api_service
from conversations.general.decorators import (
    TASK_EXECUTION,
    not_in_conversation,
    set_conversation_name,
)
from conversations.menu.decorators import user_exists
from conversations.menu.keyboards import (
    AGREE_OR_CANCEL_KEYBOARD,
    URL_BUTTON,
    create_inline_tasks_keyboard,
)
from internal_requests.entities import Problem
from utils.error_handler import error_decorator

_LOGGER = logging.getLogger(__name__)


@error_decorator(logger=_LOGGER)
async def show_done_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    task_number = int(query.data.split("_")[-1])

    await update.effective_message.edit_text(
        text="\n\n".join(
            (
                update.effective_message.text_html,
                templates.PICKED_TASK.format(task_number=task_number),
            )
        ),
    )

    task_results = await api_service.get_messages_with_results(
        update.effective_chat.id, task_number
    )
    for result in task_results:
        await update.effective_message.reply_text(text=result.content)

    del context.user_data["current_conversation"]

    return ConversationHandler.END


async def finish_tasks_conversation(
    _update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data.clear()
    return ConversationHandler.END


async def add_task_number_to_prev_message(
    update: Update,
    context: CallbackContext,
    task_number: int,
    start_task_method: Callable,
) -> int:
    message = update.effective_message
    await message.edit_text(
        text=(
            f"{message.text_html}"
            f"\n\n{templates.PICKED_TASK.format(task_number=task_number)}"
        ),
        reply_markup=message.reply_markup,
    )
    return await start_task_method(update, context)


@user_exists
@not_in_conversation(ConversationHandler.END)
@set_conversation_name("tasks")
@error_decorator(logger=_LOGGER)
async def show_all_user_tasks(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Посмотреть список заданий."""
    tasks = await api_service.get_user_task_status_list(
        telegram_id=update.effective_user.id
    )
    keyboard = create_inline_tasks_keyboard(tasks)
    if update.callback_query:
        await update.effective_message.edit_text(
            text=templates.TASKS_LIST_TEXT,
            reply_markup=keyboard,
        )
    else:
        await update.effective_message.reply_text(
            text=templates.TASKS_LIST_TEXT,
            reply_markup=keyboard,
        )
    return templates.TASKS_STATE


@user_exists
@not_in_conversation(ConversationHandler.END)
@set_conversation_name("ask")
@error_decorator(logger=_LOGGER)
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


@not_in_conversation()
@error_decorator(logger=_LOGGER)
async def show_url(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Перейти на сайт YouCan."""
    await update.message.reply_text(
        text=templates.GET_MORE_INFO_TEXT,
        reply_markup=URL_BUTTON,
    )


async def cancel_current_conversation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Optional[int]:
    """Обрабатывает команду /cancel, отменяя текущий активный диалог."""
    current_conversation = context.user_data.get("current_conversation")

    _LOGGER.info(
        "Пользователь %d использовал команду /cancel для %s",
        update.effective_chat.id,
        current_conversation or "отсутствующего диалога",
    )

    if current_conversation is None:
        await update.message.reply_text(templates.NO_ACTIVE_TASKS_MESSAGE)
        return None

    if current_conversation == TASK_EXECUTION:
        message = templates.TASK_CANCELLED_MESSAGE
    else:
        message = templates.COMMAND_CANCELLED_MESSAGE_TEMPLATE % current_conversation
    await update.message.reply_text(message)

    context.user_data.clear()
    return ConversationHandler.END
