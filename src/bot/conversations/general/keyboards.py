from telegram import ReplyKeyboardMarkup

from .templates import FIRST_TASK_BUTTON_LABEL, HELLO_BUTTON_LABEL, START_BUTTON_LABEL

HELLO_BUTTON = ReplyKeyboardMarkup([[HELLO_BUTTON_LABEL]], resize_keyboard=True)

START_BUTTON = ReplyKeyboardMarkup([[START_BUTTON_LABEL]], resize_keyboard=True)
FIRST_TASK_BUTTON = ReplyKeyboardMarkup(
    [[FIRST_TASK_BUTTON_LABEL]], resize_keyboard=True
)
