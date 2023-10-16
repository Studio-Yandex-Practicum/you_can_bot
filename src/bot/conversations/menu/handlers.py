from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    CallbackContext
)

from .decorators import user_exists

from internal_requests.entities import (
    Problem,
)

from conversations.task_1.handlers import start_task_1
from .callback_funcs import show_done_tasks, show_undone_tasks
from internal_requests.service import (
    get_info_about_user,
    get_user_task_status_list,
    update_user_info,
    create_question_from_user,
    get_messages_with_results
)

from .keyboards import (
    CONFIRMATION_BUTTONS,
    PROFILE_MENU_BUTTON,
    URL_BUTTON,
    create_tasks_keyboard,
    create_inline_tasks_keyboard,
    create_inline_buttons_agree_or_cancel,
    create_my_tasks_keyboard
)
from .templates import (
    QUESTION_CANCEL,
    SHOW_TASKS,
    ASK_ME_QUESTION_TEXT,
    CANCEL_TEXT,
    CONFIRM_PROFILE_CHANGING,
    EDIT_PROFILE,
    ENTER_NAME,
    ENTER_SURNAME,
    GET_MORE_INFO_TEXT,
    GET_NUMBER_FROM_DB,
    INCORRECT_NAME,
    MY_TASKS,
    NAME_PATTERN,
    PROFILE_CHANGED,
    QUESTION_CONFIRMATION_TEXT,
    SEND_QUESTION_TEXT,
    TASKS_LIST_TEXT,
    USER_PROFILE_TEXT,
    WAITING_FOR_NAME,
    WAITING_FOR_QUESTION,
    WAITING_FOR_SURNAME,
)


async def get_user_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Посмотреть профиль."""
    user_info = await get_info_about_user(update.effective_user.id)
    text = USER_PROFILE_TEXT.format(
        name=user_info.name,
        surname=user_info.surname,
    )
    # keyboard = ReplyKeyboardMarkup(
    #     keyboard=PROFILE_MENU_BUTTON, resize_keyboard=True, one_time_keyboard=True
    # )
    keyboard = create_my_tasks_keyboard()
    await update.message.reply_text(text=text, reply_markup=keyboard)
    return MY_TASKS


# async def edit_user_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Изменение профиля - начало диалога."""
#     await update.message.reply_text(text=ENTER_NAME)
#     return WAITING_FOR_NAME


# async def update_user_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Принимает изменения имени."""
#     user_name = update.message.text.title()
#     context.user_data["name"] = user_name
#     data = {'name': user_name}
#     await update_user_info(update.effective_user.id, data)
#     await update.message.reply_text(text=ENTER_SURNAME)
#     return WAITING_FOR_SURNAME


# async def update_user_surname(
#     update: Update, context: ContextTypes.DEFAULT_TYPE
# ) -> None:
#     """
#     Принимает изменения фамилии
#     и запрашивает подтверждение изменения профиля.
#     """
#     user_surname = update.message.text.title()
#     context.user_data["surname"] = user_surname
#     data = {'surname': user_surname}
#     keyboard = ReplyKeyboardMarkup(
#         CONFIRMATION_BUTTONS, resize_keyboard=True, one_time_keyboard=True
#     )
#     await update.message.reply_text(
#         text=CONFIRM_PROFILE_CHANGING, reply_markup=keyboard
#     )
#     await update_user_info(update.effective_user.id, data)


async def send_incorrect_data_alert(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает случаи с некорректным вводом имени или фамилии."""
    await update.message.reply_text(text=INCORRECT_NAME)


async def save_user_profile_changings(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Сохраняет новые данные пользователя в базу данных."""
    # TODO сохранение данных в базу данных из context.user_data
    context.user_data.clear()
    await update.message.reply_text(text=PROFILE_CHANGED)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отменяет внесение изменений в профиль/ отправку вопроса специалисту."""
    context.user_data.clear()
    await update.message.reply_text(text=CANCEL_TEXT)
    return ConversationHandler.END


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


async def show_all_user_results(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Посмотреть расшифровку результатов."""
    keyboard = create_tasks_keyboard()
    await update.message.reply_text(text=TASKS_LIST_TEXT, reply_markup=keyboard)


async def suggest_ask_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Задать вопрос специалисту."""
    await update.message.reply_text(ASK_ME_QUESTION_TEXT)
    return WAITING_FOR_QUESTION


async def get_user_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Подтвердить отправку вопроса"""
    context.user_data["question"] = update.message.text
    # keyboard = ReplyKeyboardMarkup(
    #     keyboard=CONFIRMATION_BUTTONS, resize_keyboard=True, one_time_keyboard=True
    # )
    keyboard = create_inline_buttons_agree_or_cancel()
    await update.message.reply_text(text=SEND_QUESTION_TEXT, reply_markup=keyboard)


async def confirm_saving_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Сохраняет вопрос в базу данных."""
    question = context.user_data['question']
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


async def show_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Перейти на сайт YouCan."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=URL_BUTTON, resize_keyboard=True, one_time_keyboard=True
    )
    await update.message.reply_text(text=GET_MORE_INFO_TEXT, reply_markup=keyboard)


async def fallback(update: Update, context: CallbackContext):
    await update.message.reply_text('Некорректный ввод. Пожалуйста, выберите одну из доступных команд.')
    return ConversationHandler.END


# async def move_back(
#     update: Update, context: ContextTypes.DEFAULT_TYPE
# ) -> int:
#     """Возвращает к работе с главным меню."""
#     context.user_data.clear()
#     await update.message.reply_text(text=MOVE_BACK_MSG)
#     return ConversationHandler.END

cancel_handler = MessageHandler(filters.Regex("^Отменить$"), cancel)
profile_handler = ConversationHandler(
    entry_points=[CommandHandler("profile", get_user_profile)],
    states={
        MY_TASKS: [
            CallbackQueryHandler(show_all_user_tasks, pattern=r"^my_tasks$")
            # MessageHandler(~filters.Regex(NAME_PATTERN), send_incorrect_data_alert)
        ]


    },
    fallbacks=[
       MessageHandler(filters.Regex(r"^[a-zA-Zа-яА-я]{1,}$"), fallback)
    ],
)

show_all_tasks_handler = ConversationHandler(
    allow_reentry=True,
    entry_points=[
        CommandHandler('tasks', show_all_user_tasks),
        # CallbackQueryHandler(start_task_1, pattern=r"^result_task_(?P<number>\d+)$")
        ],
    states={
        SHOW_TASKS: [
            CallbackQueryHandler(
                show_done_tasks, pattern=r"^result_task_(?P<number>\d+)$"
            ),
            CallbackQueryHandler(
                show_undone_tasks, pattern=r"^start_task_(?P<number>\d+)$"
            )
        ]
    },
    fallbacks=[
        MessageHandler(filters.Regex(r"^[a-zA-Zа-яА-я]{1,}$"), fallback),
    ],
    
)

# show_all_tasks_handler = CommandHandler("tasks", show_all_user_tasks)





        # EDIT_PROFILE: [
        #     MessageHandler(filters.Regex("^Редактировать профиль$"), edit_user_profile)
        # ],
        # WAITING_FOR_NAME: [
        #     MessageHandler(
        #         filters.Regex(NAME_PATTERN)
        #         & ~filters.Regex("^(Подтвердить|Отменить)$"),
        #         update_user_name,
        #     ),
        #     MessageHandler(~filters.Regex(NAME_PATTERN), send_incorrect_data_alert),
        # ],
        # WAITING_FOR_SURNAME: [
        #     MessageHandler(
        #         filters.Regex(NAME_PATTERN)
        #         & ~filters.Regex("^(Подтвердить|Отменить)$"),
        #         update_user_surname,
        #     ),
        #     MessageHandler(~filters.Regex(NAME_PATTERN), send_incorrect_data_alert),
        # ],

ask_question_handler = ConversationHandler(
    entry_points=[
        CommandHandler("ask", suggest_ask_question)
        ],
    states={
        WAITING_FOR_QUESTION: [
            MessageHandler(
                filters.TEXT
                & ~filters.COMMAND
                & ~filters.Regex("^(Подтвердить|Отменить)$"),
                get_user_question,
            )
        ],
    },
    fallbacks=[
        CallbackQueryHandler(confirm_saving_question, pattern=r"^agree_question$"),
        # MessageHandler(filters.Regex('^Отменить$'), cancel)
        CallbackQueryHandler(cancel_save_question, pattern=r"^cancel_question$")
    ],
)

# show_all_tasks_handler = CommandHandler("tasks", show_all_user_tasks)
show_user_results_handler = CommandHandler("results", show_all_user_results)
info_handler = CommandHandler("info", show_url)
