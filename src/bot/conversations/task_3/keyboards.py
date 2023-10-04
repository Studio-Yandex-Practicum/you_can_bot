from telegram import InlineKeyboardButton, InlineKeyboardMarkup

CANCEL_LOG_TEXT = "Пользователь %s закончил диалог."
CANCEL_COMMAND = "cancel"
GO_TO_TASK_4_KEYBOARD = InlineKeyboardMarkup(
    ((InlineKeyboardButton(text="ЗАДАНИЕ 4", callback_data="ЗАДАНИЕ 4"),),)
)
NEXT_KEYBOARD = InlineKeyboardMarkup(
    ((InlineKeyboardButton(text="Далее", callback_data="Далее"),),)
)
REPLY_KEYBOARD = InlineKeyboardMarkup(
    (
        (
            InlineKeyboardButton(text="А", callback_data="а"),
            InlineKeyboardButton(text="Б", callback_data="б"),
        ),
    ),
)
TEXT_ENTRY_POINT_BUTTON_FOR_TASK_3 = "ЗАДАНИЕ 3"
