from telegram import BotCommand, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from .templates import (
    CANCEL,
    COMMANDS,
    CONFIRM,
    EDIT_PROFILE_TEXT,
    TASKS_BUTTON_TEXT,
    TASKS_NUMBER,
    URL,
    URL_BUTTON_TEXT,
)

CANCEL_BUTTON = [KeyboardButton(text=CANCEL)]

PROFILE_MENU_BUTTONS = [[KeyboardButton(text=EDIT_PROFILE_TEXT)], CANCEL_BUTTON]

CONFIRMATION_BUTTONS = [[KeyboardButton(text=CONFIRM)], CANCEL_BUTTON]

URL_BUTTON = [[KeyboardButton(text=URL_BUTTON_TEXT, web_app=WebAppInfo(url=URL))]]


def get_main_menu_commands() -> list[BotCommand]:
    """Создает кнопку с меню бота и добавляет в нее команды."""
    return [BotCommand(cmd, description) for cmd, description in COMMANDS.items()]


def create_tasks_keyboard() -> ReplyKeyboardMarkup:
    """Формирует клавиатуру со списком заданий."""
    tasks_list_buttons = [
        [KeyboardButton(text=f"{TASKS_BUTTON_TEXT} {i + 1}")]
        for i in range(TASKS_NUMBER)
    ] + [CANCEL_BUTTON]
    return ReplyKeyboardMarkup(
        keyboard=tasks_list_buttons, resize_keyboard=True, one_time_keyboard=True
    )
