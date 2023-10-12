from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from conversations import CANCEL, CANCEL_BUTTON_LABEL

from .templates import (
    FIRST_TASK_BUTTON_LABEL,
    GO_BUTTON_LABEL,
    HELLO_BUTTON_LABEL,
    START_ACQUAINTANCE,
    START_SKILL_SETS,
)

HELLO_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(HELLO_BUTTON_LABEL, callback_data=START_ACQUAINTANCE)],
        [InlineKeyboardButton(CANCEL_BUTTON_LABEL, callback_data=CANCEL)],
    ],
)
START_SKILL_SETS_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(GO_BUTTON_LABEL, callback_data=START_SKILL_SETS)],
        [InlineKeyboardButton(CANCEL_BUTTON_LABEL, callback_data=CANCEL)],
    ],
)
FIRST_TASK_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(FIRST_TASK_BUTTON_LABEL, callback_data="start_task_1")]
    ],
)
