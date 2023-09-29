from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

ANSWER = "Ответ пользователя %s на %s вопрос: %s"
CANSEL = "Пользователь %s закончил диалог."
CANCEL_COMMAND = "cancel"
CANCEL_KEYBOARD = ReplyKeyboardRemove()
NEXT_KEYBOARD = InlineKeyboardMarkup(
    ((InlineKeyboardButton(text="Далее", callback_data="Далее"),),)
)
REPLY_KEYBOARD = InlineKeyboardMarkup(
    (
        (
            InlineKeyboardButton(text="А", callback_data="А"),
            InlineKeyboardButton(text="Б", callback_data="Б"),
        ),
    ),
)
TEXT_ENTRY_POINT_BUTTON_FOR_TASK_3 = "ЗАДАНИЕ 3"
