from telegram import InlineKeyboardButton, InlineKeyboardMarkup

CANCEL_LOG_TEXT = "Пользователь %s закончил диалог."
CANCEL_COMMAND = "cancel"
NEXT_KEYBOARD = InlineKeyboardMarkup(
    ((InlineKeyboardButton(text="Далее", callback_data="Далее"),),)
)
REPLY_KEYBOARD = InlineKeyboardMarkup.from_row(
    (
        InlineKeyboardButton(text="А", callback_data="а"),
        InlineKeyboardButton(text="Б", callback_data="б"),
    ),
)
TEXT_ENTRY_POINT_BUTTON_FOR_TASK_8 = "Задание 8"
