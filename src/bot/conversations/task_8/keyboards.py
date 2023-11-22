from telegram import InlineKeyboardButton, InlineKeyboardMarkup

CANCEL_LOG_TEXT = "Пользователь %s закончил диалог."
CANCEL_COMMAND = "cancel"
NEXT_KEYBOARD = InlineKeyboardMarkup(
    ((InlineKeyboardButton(text="Далее", callback_data="Далее"),),)
)
FIRST_STAGE_END_KEYBOARD = InlineKeyboardMarkup(
    (
        (
            InlineKeyboardButton(
                text="Перейти ко второму кругу задания", callback_data="next_stage"
            ),
        ),
    )
)
SECOND_STAGE_END_KEYBOARD = InlineKeyboardMarkup(
    (
        (
            InlineKeyboardButton(
                text="Перейти к последнему кругу задания", callback_data="next_stage"
            ),
        ),
    )
)
TASK_END_KEYBOARD = InlineKeyboardMarkup(
    (
        (
            InlineKeyboardButton(
                text="Посмотреть результат", callback_data="finish_task_8"
            ),
        ),
    )
)
REPLY_KEYBOARD = InlineKeyboardMarkup.from_row(
    (
        InlineKeyboardButton(text="А", callback_data="а"),
        InlineKeyboardButton(text="Б", callback_data="б"),
    ),
)
TEXT_ENTRY_POINT_BUTTON_FOR_TASK_8 = "Задание 8"
