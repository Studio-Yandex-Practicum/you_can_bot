from telegram import ReplyKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from internal_requests.entities import Problem
from internal_requests.service import (
    create_question_from_user,
    get_info_about_user,
    get_user_task_status_list,
)

from .callback_funcs import show_done_tasks, show_undone_tasks
from .decorators import user_exists
from .keyboards import (
    AGREE_OR_CANCEL_KEYBOARD,
    MY_TASKS_KEYBOARD,
    URL_BUTTON,
    create_inline_tasks_keyboard,
)
from .templates import (
    ASK_ME_QUESTION_TEXT,
    GET_MORE_INFO_TEXT,
    MY_TASKS_START,
    QUESTION_CANCEL,
    QUESTION_CONFIRMATION_TEXT,
    SEND_QUESTION_TEXT,
    SHOW_TASKS,
    TASKS_LIST_TEXT,
    USER_PROFILE_TEXT,
    WAITING_FOR_QUESTION,
)


@user_exists
async def get_user_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Посмотреть профиль."""
    user_info = await get_info_about_user(update.effective_user.id)
    text = USER_PROFILE_TEXT.format(name=user_info.name, surname=user_info.surname)
    await update.message.reply_text(
        text=text, reply_markup=MY_TASKS_KEYBOARD, parse_mode=ParseMode.HTML
    )
    return MY_TASKS_START


@user_exists
async def show_all_user_tasks(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Посмотреть список заданий."""
    tasks = await get_user_task_status_list(telegram_id=update.effective_user.id)
    keyboard = create_inline_tasks_keyboard(tasks)
    if update.callback_query:
        await update.callback_query.message.edit_text(
            text=TASKS_LIST_TEXT, reply_markup=keyboard
        )
    else:
        await update.effective_message.reply_text(
            text=TASKS_LIST_TEXT, reply_markup=keyboard
        )
    return SHOW_TASKS


@user_exists
async def suggest_ask_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Задать вопрос специалисту."""
    await update.message.reply_text(ASK_ME_QUESTION_TEXT)
    return WAITING_FOR_QUESTION


async def get_user_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Подтвердить отправку вопроса"""
    context.user_data["question"] = update.message.text
    await update.message.reply_text(
        text=SEND_QUESTION_TEXT, reply_markup=AGREE_OR_CANCEL_KEYBOARD
    )


async def confirm_saving_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Сохраняет вопрос в базу данных."""
    question = context.user_data["question"]
    problem = Problem(telegram_id=update.effective_user.id, message=question)
    await create_question_from_user(problem)
    context.user_data.clear()
    await update.callback_query.message.edit_text(text=QUESTION_CONFIRMATION_TEXT)
    return ConversationHandler.END


async def cancel_save_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отменяет отправку вопроса."""
    context.user_data.clear()
    await update.callback_query.message.edit_text(text=QUESTION_CANCEL)
    return ConversationHandler.END


@user_exists
async def show_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Перейти на сайт YouCan."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=URL_BUTTON, resize_keyboard=True, one_time_keyboard=True
    )
    await update.message.reply_text(text=GET_MORE_INFO_TEXT, reply_markup=keyboard)


async def fallback(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Некорректный ввод. Пожалуйста, выберите одну из доступных команд."
    )
    return ConversationHandler.END


# /profile
profile_handler = ConversationHandler(
    allow_reentry=True,
    entry_points=[CommandHandler("profile", get_user_profile)],
    states={
        MY_TASKS_START: [
            CallbackQueryHandler(show_all_user_tasks, pattern=r"^my_tasks$")
        ]
    },
    fallbacks=[MessageHandler(filters.Regex(r"^[a-zA-Zа-яА-я]{1,}$"), fallback)],
)
# /tasks
show_all_tasks_handler = ConversationHandler(
    allow_reentry=True,
    entry_points=[
        CommandHandler("tasks", show_all_user_tasks),
        CallbackQueryHandler(show_done_tasks, pattern=r"^result_task_(?P<number>\d+)$"),
        CallbackQueryHandler(
            show_undone_tasks, pattern=r"^start_task_(?P<number>\d+)$"
        ),
    ],
    states={
        SHOW_TASKS: [
            CallbackQueryHandler(
                show_done_tasks, pattern=r"^result_task_(?P<number>\d+)$"
            ),
            CallbackQueryHandler(
                show_undone_tasks, pattern=r"^start_task_(?P<number>\d+)$"
            ),
        ]
    },
    fallbacks=[
        MessageHandler(filters.Regex(r"^[a-zA-Zа-яА-я]{1,}$"), fallback),
    ],
)
# /ask
ask_question_handler = ConversationHandler(
    entry_points=[CommandHandler("ask", suggest_ask_question)],
    states={
        WAITING_FOR_QUESTION: [
            MessageHandler(
                filters.TEXT,
                get_user_question,
            )
        ],
    },
    fallbacks=[
        CallbackQueryHandler(confirm_saving_question, pattern=r"^agree_question$"),
        CallbackQueryHandler(cancel_save_question, pattern=r"^cancel_question$"),
    ],
)
# /info
info_handler = CommandHandler("info", show_url)
