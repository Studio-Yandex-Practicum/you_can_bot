import re

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from .templates import (
    YOUR_NAME_QUESTION,
    SKILL_SET_INFORMATION,
    FIRST_SKILL_SET_INFORMATION,
    START_BUTTON_LABEL,
    FIRST_TASK_BUTTON_LABEL,
    CANCEL_ACQUAINTANCE,
    START_MESSAGE,
    HELLO_BUTTON_LABEL,
    WRONG_NAME_SURNAME,
    ILLEGAL_CHARACTERS_NAME_SURNAME,
)

from .keyboards import HELLO_BUTTON, START_BUTTON, FIRST_TASK_BUTTON


HELLO, NAME, START, FIRST_TASK = range(4)

REGEXP_NAME_SURNAME = r"^[а-яА-ЯёЁa-zA-Z]+$"


async def start(update, context) -> None:
    """Первое сообщение от бота при вводе команды /start."""
    await update.message.reply_text(START_MESSAGE, reply_markup=HELLO_BUTTON)
    return HELLO


async def start_acquaintance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Спрашивает имя у пользователя."""
    await update.message.reply_text(
        YOUR_NAME_QUESTION, reply_markup=ReplyKeyboardRemove()
    )
    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняет предоставленное имя и фамилию в контексте
    и знакомит пользователя со скиллсетами."""
    user_input_data = update.message.text.title().split()

    if len(user_input_data) != 2:
        await update.message.reply_text(WRONG_NAME_SURNAME)
        return NAME

    for element in user_input_data:
        if re.search(REGEXP_NAME_SURNAME, element) is None:
            await update.message.reply_text(ILLEGAL_CHARACTERS_NAME_SURNAME)
            return NAME

    user_name, user_surname = user_input_data

    context.user_data["user_name"] = user_name
    context.user_data["user_surname"] = user_surname
    await update.message.reply_text(
        SKILL_SET_INFORMATION.format(f"{user_name}"), reply_markup=START_BUTTON
    )
    return START


async def start_skill_sets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выдает краткое описание первого задания
    и предлагает к нему приступить."""
    await update.message.reply_text(
        FIRST_SKILL_SET_INFORMATION, reply_markup=FIRST_TASK_BUTTON
    )
    return FIRST_TASK


async def first_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Тут происходит:
    1. Формирование JSON с информацией по пользователю.
    2. Отправка этой информации на Django API.
    3. Завершение conversation handler знакомства.
    4. Запуск conversation handler первого задания.

    На данный момент реализован 1 и 3 пункт.
    """

    data = {
        "name": context.user_data["user_name"],
        "surname": context.user_data["user_surname"],
        "telegram_id": update.effective_chat.id,
    }

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Завершает диалог с пользователем."""
    context.user_data.clear()
    await update.message.reply_text(
        CANCEL_ACQUAINTANCE, reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


acquaintance_handler: ConversationHandler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        HELLO: [MessageHandler(filters.Regex(HELLO_BUTTON_LABEL), start_acquaintance)],
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
        START: [MessageHandler(filters.Regex(START_BUTTON_LABEL), start_skill_sets)],
        FIRST_TASK: [
            MessageHandler(filters.Regex(FIRST_TASK_BUTTON_LABEL), first_task)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
