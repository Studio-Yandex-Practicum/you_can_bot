from telegram import (
    BotCommand, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo)

from . templates import (
    COMMANDS, TASKS_BUTTON_TEXT, TASKS_NUMBER,
    MOVE_BACK_TEXT, EDIT_PROFILE_TEXT,
    URL, URL_BUTTON_TEXT, CONFIRM, CANCEL
)


MOVE_BACK_BUTTON = [
    [KeyboardButton(text=MOVE_BACK_TEXT)]
]

PROFILE_MENU_BUTTONS = [
    [KeyboardButton(text=EDIT_PROFILE_TEXT)]
] + MOVE_BACK_BUTTON

CONFIRMATION_BUTTONS = [
    [KeyboardButton(text=CONFIRM)],
    [KeyboardButton(text=CANCEL)]
]

URL_BUTTON = [
    [KeyboardButton(
        text=URL_BUTTON_TEXT,
        web_app=WebAppInfo(url=URL)
    )]
]


def get_main_menu_commands() -> list[BotCommand]:
    """Создает кнопку с меню бота и добавляет в нее команды."""
    return [
        BotCommand(cmd, description) for cmd, description in COMMANDS.items()
    ]


def create_tasks_keyboard() -> ReplyKeyboardMarkup:
    """Формирует клавиатуру со списком заданий."""
    tasks_list_buttons = [
        [
            KeyboardButton(text=f'{TASKS_BUTTON_TEXT} {i+1}')
        ] for i in range(TASKS_NUMBER)
    ] + MOVE_BACK_BUTTON
    return ReplyKeyboardMarkup(
        keyboard=tasks_list_buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )
