from telegram import InlineKeyboardButton, InlineKeyboardMarkup

CANCEL_LOG_TEXT = "Пользователь %s закончил диалог."
CANCEL_COMMAND = "cancel"
GO_TO_TASK_3_KEYBOARD = InlineKeyboardMarkup(
    ((InlineKeyboardButton(text="Задание 3", callback_data="start_task_3"),),)
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
    )
)
TEXT_ENTRY_POINT_BUTTON_FOR_TASK_2 = "Задание 2"
