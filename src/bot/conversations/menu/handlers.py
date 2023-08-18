from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler, ConversationHandler, MessageHandler, ContextTypes, filters)

from .keyboards import (
    PROFILE_MENU_BUTTONS, URL_BUTTON, CONFIRMATION_BUTTONS,
    create_tasks_keyboard)
from .templates import (
    USER_PROFILE_TEXT, GET_NUMBER_FROM_DB, TASKS_LIST_TEXT, CANCEL_TEXT,
    ASK_ME_QUESTION_TEXT, GET_MORE_INFO_TEXT, EDIT_PROFILE, ENTER_NAME,
    WAITING_FOR_NAME, WAITING_FOR_SURNAME, ENTER_SURNAME, INCORRECT_NAME,
    WAITING_FOR_QUESTION, CONFIRM_PROFILE_CHANGING, PROFILE_CHANGED,
    SEND_QUESTION_TEXT, QUESTION_CONFIRMATION_TEXT, NAME_PATTERN)


async def get_user_profile(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Посмотреть профиль."""
    text = USER_PROFILE_TEXT.format(
            # TODO get user name and number from data base
            name=update.effective_user.first_name,
            tasks_completed=GET_NUMBER_FROM_DB
    )
    keyboard = ReplyKeyboardMarkup(
        keyboard=PROFILE_MENU_BUTTONS,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(text=text, reply_markup=keyboard)
    return EDIT_PROFILE


async def edit_user_profile(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Изменение профиля - начало диалога."""
    await update.message.reply_text(text=ENTER_NAME)
    return WAITING_FOR_NAME


async def update_user_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Принимает изменения имени."""
    user_name = update.message.text.title()
    context.user_data['name'] = user_name
    await update.message.reply_text(text=ENTER_SURNAME)
    return WAITING_FOR_SURNAME


async def update_user_surname(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Принимает изменения фамилии
    и запрашивает подтверждение изменения профиля.
    """
    user_surname = update.message.text.title()
    context.user_data['surname'] = user_surname
    keyboard = ReplyKeyboardMarkup(
        CONFIRMATION_BUTTONS,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=CONFIRM_PROFILE_CHANGING,
        reply_markup=keyboard
    )


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


async def cancel(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отменяет внесение изменений в профиль/ отправку вопроса специалисту."""
    context.user_data.clear()
    await update.message.reply_text(text=CANCEL_TEXT)
    return ConversationHandler.END


async def show_all_user_tasks(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Посмотреть список заданий."""
    keyboard = create_tasks_keyboard()
    await update.message.reply_text(
        text=TASKS_LIST_TEXT, reply_markup=keyboard
    )


async def show_all_user_results(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Посмотреть расшифровку результатов."""
    keyboard = create_tasks_keyboard()
    await update.message.reply_text(
        text=TASKS_LIST_TEXT, reply_markup=keyboard
    )


async def suggest_ask_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Задать вопрос специалисту."""
    await update.message.reply_text(ASK_ME_QUESTION_TEXT)
    return WAITING_FOR_QUESTION


async def get_user_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Подтвердить отправку вопроса"""
    context.user_data['question'] = update.message.text
    keyboard = ReplyKeyboardMarkup(
        keyboard=CONFIRMATION_BUTTONS,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=SEND_QUESTION_TEXT,
        reply_markup=keyboard
    )


async def confirm_saving_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Сохраняет вопрос в базу данных."""
    # TODO сохранение данных в базу данных из context.user_data
    context.user_data.clear()
    await update.message.reply_text(text=QUESTION_CONFIRMATION_TEXT)
    return ConversationHandler.END


async def show_url(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Перейти на сайт YouCan."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=URL_BUTTON,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text(
        text=GET_MORE_INFO_TEXT, reply_markup=keyboard
    )


# async def move_back(
#     update: Update, context: ContextTypes.DEFAULT_TYPE
# ) -> int:
#     """Возвращает к работе с главным меню."""
#     context.user_data.clear()
#     await update.message.reply_text(text=MOVE_BACK_MSG)
#     return ConversationHandler.END

cancel_handler = MessageHandler(filters.Regex('^Отменить$'), cancel)
profile_handler = ConversationHandler(
    entry_points=[
        CommandHandler('profile', get_user_profile)
    ],
    states={
        EDIT_PROFILE: [
            MessageHandler(
                filters.Regex('^Редактировать профиль$'),
                edit_user_profile
            )
        ],
        WAITING_FOR_NAME: [
            MessageHandler(
                filters.Regex(NAME_PATTERN) & ~filters.Regex(
                    '^(Подтвердить|Отменить)$'),
                update_user_name
            ),
            MessageHandler(
                ~filters.Regex(NAME_PATTERN), send_incorrect_data_alert
            ),
        ],
        WAITING_FOR_SURNAME: [
            MessageHandler(
                filters.Regex(NAME_PATTERN) & ~filters.Regex(
                    '^(Подтвердить|Отменить)$'),
                update_user_surname
            ),
            MessageHandler(
                ~filters.Regex(NAME_PATTERN), send_incorrect_data_alert
            ),
        ]
    },
    fallbacks=[
        MessageHandler(
            filters.Regex('^Подтвердить$'),
            save_user_profile_changings),
        # MessageHandler(filters.Regex('^Отменить$'), cancel)
        cancel_handler
    ],
)

ask_question_handler = ConversationHandler(
    entry_points=[
        CommandHandler('ask', suggest_ask_question)
    ],
    states={
        WAITING_FOR_QUESTION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND & ~filters.Regex(
                    '^(Подтвердить|Отменить)$'),
                get_user_question)
        ],
    },
    fallbacks=[
        MessageHandler(
            filters.Regex('^Подтвердить$'), confirm_saving_question),
        # MessageHandler(filters.Regex('^Отменить$'), cancel)
        cancel_handler
    ],
)

show_all_tasks_handler = CommandHandler('tasks', show_all_user_tasks)
show_user_results_handler = CommandHandler('results', show_all_user_results)
info_handler = CommandHandler('info', show_url)
