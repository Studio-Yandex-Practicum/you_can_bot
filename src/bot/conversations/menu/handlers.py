from telegram import Update, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler, ConversationHandler, MessageHandler, ContextTypes,
    CallbackQueryHandler, filters)

from .keyboards import (
    PROFILE_MENU_BUTTONS, URL_BUTTON, CONFIRMATION_BUTTONS,
    create_tasks_keyboard)
from .templates import (
    USER_PROFILE_TEXT, GET_NUMBER_FROM_DB, TASKS_LIST_TEXT,
    ASK_ME_QUESTION_TEXT, GET_MORE_INFO_TEXT, EDIT_PROFILE, ENTER_NAME,
    WAITING_FOR_NAME, EDIT_PROFILE_CALLBACK, CONFIRM_CALLBACK, CANCEL_CALLBACK,
    WAITING_FOR_QUESTION, NEW_NAME, INCORRECT_NAME, NAME_CHANGED, CANCEL_TEXT,
    SEND_QUESTION_TEXT, QUESTION_CONFIRMATION_TEXT, MOVE_BACK_MSG,
    MOVE_BACK_CALLBACK)


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Посмотреть профиль."""
    text = USER_PROFILE_TEXT.format(
            # TODO get user name and number from data base
            name=update.effective_user.first_name,
            tasks_completed=GET_NUMBER_FROM_DB
    )
    keyboard = InlineKeyboardMarkup(PROFILE_MENU_BUTTONS)
    await update.message.reply_text(text=text, reply_markup=keyboard)
    return EDIT_PROFILE


async def edit_profile(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Изменение профиля - точка входа."""
    await update.callback_query.edit_message_text(text=ENTER_NAME)
    return WAITING_FOR_NAME


async def update_profile(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Принимает изменения профиля и запрашивает подтверждение."""
    user_name = update.message.text.capitalize()
    context.user_data['name'] = user_name
    keyboard = InlineKeyboardMarkup(CONFIRMATION_BUTTONS)
    await update.message.reply_text(
        text=NEW_NAME.format(user_name=user_name),
        reply_markup=keyboard
    )


async def incorrect_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает случаи с некорректным вводом имени."""
    await update.message.reply_text(text=INCORRECT_NAME)


async def confirm_name(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Сохраняет новые данные пользователя в базу данных."""
    # TODO сохранение данных в базу данных из context.user_data
    context.user_data.clear()
    await update.callback_query.edit_message_text(text=NAME_CHANGED)
    return ConversationHandler.END


async def cancel(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отменяет внесение изменений в профиль/ отправку вопроса специалисту."""
    context.user_data.clear()
    await update.callback_query.edit_message_text(text=CANCEL_TEXT)
    return ConversationHandler.END


async def all_tasks(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Посмотреть список заданий."""
    keyboard = create_tasks_keyboard(prefix='do')
    await update.message.reply_text(
        text=TASKS_LIST_TEXT, reply_markup=keyboard
    )


async def my_results(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Посмотреть расшифровку результатов."""
    keyboard = create_tasks_keyboard(prefix='results')
    await update.message.reply_text(
        text=TASKS_LIST_TEXT, reply_markup=keyboard
    )


async def ask(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Задать вопрос специалисту."""
    await update.message.reply_text(ASK_ME_QUESTION_TEXT)
    return WAITING_FOR_QUESTION


async def get_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Подтвердить отправку вопроса"""
    context.user_data['question'] = update.message.text
    keyboard = InlineKeyboardMarkup(CONFIRMATION_BUTTONS)
    await update.message.reply_text(
        text=SEND_QUESTION_TEXT,
        reply_markup=keyboard
    )


async def confirm_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Сохраняет вопрос в базу данных."""
    # TODO сохранение данных в базу данных из context.user_data
    context.user_data.clear()
    await update.callback_query.edit_message_text(
        text=QUESTION_CONFIRMATION_TEXT
    )
    return ConversationHandler.END


async def info(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Перейти на сайт YouCan."""
    keyboard = InlineKeyboardMarkup(URL_BUTTON)
    await update.message.reply_text(
        text=GET_MORE_INFO_TEXT, reply_markup=keyboard
    )


async def back(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возвращает к работе с главным меню."""
    context.user_data.clear()
    await update.callback_query.edit_message_text(text=MOVE_BACK_MSG)
    return ConversationHandler.END


profile_handler = ConversationHandler(
    entry_points=[
        CommandHandler('profile', profile)
    ],
    states={
        EDIT_PROFILE: [
            CallbackQueryHandler(
                edit_profile, pattern='^' + EDIT_PROFILE_CALLBACK + '$'
            )
        ],
        WAITING_FOR_NAME: [
            MessageHandler(
                filters.Regex('^[A-Za-zА-яЁё ]+$'), update_profile
            ),
            MessageHandler(
                ~filters.Regex('^[A-Za-zА-яЁё ]+$'), incorrect_name
            ),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            confirm_name, pattern='^' + CONFIRM_CALLBACK + '$'
        ),
        CallbackQueryHandler(
            cancel, pattern='^' + CANCEL_CALLBACK + '$'
        ),
        CallbackQueryHandler(
            back, pattern='^' + MOVE_BACK_CALLBACK + '$'
        )
    ],
)

ask_handler = ConversationHandler(
    entry_points=[
        CommandHandler('ask', ask)
    ],
    states={
        WAITING_FOR_QUESTION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_question)
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            confirm_question, pattern='^' + CONFIRM_CALLBACK + '$'
        ),
        CallbackQueryHandler(
            cancel, pattern='^' + CANCEL_CALLBACK + '$'
        ),
        CallbackQueryHandler(
            back, pattern='^' + MOVE_BACK_CALLBACK + '$'
        )
    ],
)

all_tasks_handler = CommandHandler('all_tasks', all_tasks)
my_results_handler = CommandHandler('my_results', my_results)
info_handler = CommandHandler('info', info)
move_back_handler = CallbackQueryHandler(back, pattern='^' + 'MOVE_BACK' + '$')


# Ниже - хендлеры для перехода по нажатию кнопки в соответствующее задание
# для их выполнения или просмотра результатов
# TODO
# перенести каждую из них в точку входа в соответствующий ConversationHandler

# start_task_1_handler = CallbackQueryHandler(
#     start_task_1, pattern='^' + 'do_'+ 'TASK_1' + '$')
# start_task_2_handler = CallbackQueryHandler(
#     start_task_2, pattern='^' + 'do_'+ 'TASK_2' + '$')
# start_task_3_handler = CallbackQueryHandler(
#     start_task_3, pattern='^' + 'do_'+ 'TASK_3' + '$')
# start_task_4_handler = CallbackQueryHandler(
#     start_task_4, pattern='^' + 'do_'+ 'TASK_4' + '$')
# start_task_5_handler = CallbackQueryHandler(
#     start_task_5, pattern='^' + 'do_'+ 'TASK_5' + '$')
# start_task_6_handler = CallbackQueryHandler(
#     start_task_6, pattern='^' + 'do_'+ 'TASK_6' + '$')
# start_task_7_handler = CallbackQueryHandler(
#     start_task_7, pattern='^' + 'do_'+ 'TASK_7' + '$')
# start_task_8_handler = CallbackQueryHandler(
#     start_task_8, pattern='^' + 'do_'+ 'TASK_8' + '$')

# results_task_1_handler = CallbackQueryHandler(
#     results_task_1, pattern='^' + 'results_'+ 'TASK_1' +'$')
# results_task_2_handler = CallbackQueryHandler(
#     results_task_2, pattern='^' + 'results_'+ 'TASK_2' +'$')
# results_task_3_handler = CallbackQueryHandler(
#     results_task_3, pattern='^' + 'results_'+ 'TASK_3' +'$')
# results_task_4_handler = CallbackQueryHandler(
#     results_task_4, pattern='^' + 'results_'+ 'TASK_4' +'$')
# results_task_5_handler = CallbackQueryHandler(
#     results_task_5, pattern='^' + 'results_'+ 'TASK_5' +'$')
# results_task_6_handler = CallbackQueryHandler(
#     results_task_6, pattern='^' + 'results_'+ 'TASK_6' +'$')
# results_task_7_handler = CallbackQueryHandler(
#     results_task_7, pattern='^' + 'results_'+ 'TASK_7' +'$')
# results_task_8_handler = CallbackQueryHandler(
#     results_task_8, pattern='^' + 'results_'+ 'TASK_8' +'$')
