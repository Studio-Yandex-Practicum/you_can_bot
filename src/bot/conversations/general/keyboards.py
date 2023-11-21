from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .templates import FIRST_TASK_BUTTON_LABEL, HELLO_BUTTON_LABEL, SHOW_SKILL_SET_INFO

HELLO_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                HELLO_BUTTON_LABEL,
                callback_data=SHOW_SKILL_SET_INFO,
            )
        ],
    ],
)
FIRST_TASK_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(FIRST_TASK_BUTTON_LABEL, callback_data="start_task_1")]
    ],
)
