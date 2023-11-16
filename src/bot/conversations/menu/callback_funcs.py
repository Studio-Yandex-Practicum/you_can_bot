from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import conversations.menu.templates as templates
import internal_requests.service as api_service
from conversations.menu.decorators import user_exists
from conversations.menu.keyboards import (
    AGREE_OR_CANCEL_KEYBOARD,
    MY_TASKS_KEYBOARD,
    URL_BUTTON,
    create_inline_tasks_keyboard,
)
from internal_requests.entities import Problem


async def show_done_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    task_number = int(query.data.split("_")[-1])

    await query.message.edit_text(
        text="\n\n".join(
            (
                query.message.text_html,
                templates.PICKED_TASK.format(task_number=task_number),
            )
        ),
        parse_mode=ParseMode.HTML,
    )

    task_results = await api_service.get_messages_with_results(
        query.message.chat.id, task_number
    )
    for result in task_results:
        await query.message.reply_text(text=result.content, parse_mode=ParseMode.HTML)

    return ConversationHandler.END


@user_exists
async def get_user_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Посмотреть профиль."""
    user_info = await api_service.get_info_about_user(update.effective_user.id)
    text = templates.USER_PROFILE_TEXT.format(
        name=user_info.name, surname=user_info.surname
    )
    await update.message.reply_text(
        text=text, reply_markup=MY_TASKS_KEYBOARD, parse_mode=ParseMode.HTML
    )
    return templates.SHOW_MY_TASKS_STATE


@user_exists
async def show_all_user_tasks(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Посмотреть список заданий."""
    tasks = await api_service.get_user_task_status_list(
        telegram_id=update.effective_user.id
    )
    keyboard = create_inline_tasks_keyboard(tasks)
    if update.callback_query:
        await update.callback_query.message.edit_text(
            text=templates.TASKS_LIST_TEXT, reply_markup=keyboard
        )
    else:
        await update.effective_message.reply_text(
            text=templates.TASKS_LIST_TEXT, reply_markup=keyboard
        )
    return templates.TASKS_STATE


@user_exists
async def suggest_ask_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Задать вопрос специалисту."""
    await update.message.reply_text(templates.ASK_ME_QUESTION_TEXT)
    return templates.WAITING_FOR_QUESTION_STATE


async def get_user_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Просит подтвердить отправку вопроса психологу, также обновляет его в
    случае, если пользователь изменил изначальный вопрос.
    """
    # извлекаем из контекста id изначального вопроса, если он был
    original_question_id = context.user_data.get("question_id")
    question_text = None
    question_id = None

    if update.message:  # вопрос отправлен в первый раз
        question_text = update.message.text
        question_id = update.message.message_id
    elif (
        update.edited_message
        and update.edited_message.message_id == original_question_id
    ):  # изначальный вопрос был изменён
        question_text = update.edited_message.text
        question_id = update.edited_message.message_id
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=context.user_data.get("confirmation_message_id"),
            text="\n".join((templates.SEND_QUESTION_TEXT, question_text)),
            reply_markup=AGREE_OR_CANCEL_KEYBOARD,
        )
    else:  # иные случаи
        return

    if question_text and question_id:
        context.user_data["question"] = question_text
        context.user_data["question_id"] = question_id
        if not context.user_data.get("confirmation_message_id") and update.message:
            confirmation_message = await update.message.reply_text(
                text="\n".join((templates.SEND_QUESTION_TEXT, question_text)),
                reply_markup=AGREE_OR_CANCEL_KEYBOARD,
            )
            context.user_data[
                "confirmation_message_id"
            ] = confirmation_message.message_id


async def confirm_saving_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Сохраняет вопрос в базу данных."""
    question = context.user_data["question"]
    problem = Problem(telegram_id=update.effective_user.id, message=question)
    await api_service.create_question_from_user(problem)
    context.user_data.clear()
    await update.callback_query.message.edit_text(
        text=templates.QUESTION_CONFIRMATION_TEXT
    )
    return ConversationHandler.END


async def cancel_save_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отменяет отправку вопроса."""
    context.user_data.clear()
    await update.callback_query.message.edit_text(text=templates.QUESTION_CANCEL)
    return ConversationHandler.END


@user_exists
async def show_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Перейти на сайт YouCan."""
    await update.message.reply_text(
        text=templates.GET_MORE_INFO_TEXT, reply_markup=URL_BUTTON
    )
