from telegram import BotCommand, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup

from .templates import (
    CANCEL,
    COMMANDS,
    CONFIRM,
    EDIT_PROFILE_TEXT,
    PATTERN_DONE,
    PATTERN_UNDONE,
    TASKS_BUTTON_TEXT,
    TASKS_NUMBER,
    URL,
    URL_BUTTON_TEXT,
    MY_TASKS
)

CANCEL_BUTTON = [KeyboardButton(text=CANCEL)]

PROFILE_MENU_BUTTON = [[KeyboardButton(text=MY_TASKS)]]

CONFIRMATION_BUTTONS = [[KeyboardButton(text=CONFIRM)], CANCEL_BUTTON]

URL_BUTTON = [[KeyboardButton(text=URL_BUTTON_TEXT, web_app=WebAppInfo(url=URL))]]


def get_main_menu_commands() -> list[BotCommand]:
    """Создает кнопку с меню бота и добавляет в нее команды."""
    return [BotCommand(cmd, description) for cmd, description in COMMANDS.items()]


def create_inline_tasks_keyboard(tasks):
    tasks_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=(
                        f"{'✅' if info.is_done else '❌'} "
                        f"{TASKS_BUTTON_TEXT + ' ' + str(info.number)}"
                    ),
                    callback_data=(
                        (PATTERN_DONE if info.is_done else PATTERN_UNDONE) +
                        str(info.number)
                    )
                )
                ]
            for info in tasks
        ]
    )
    return tasks_keyboard


def create_inline_buttons_agree_or_cancel():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подтвердить",
                    callback_data="agree_question"
                ),
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data="cancel_question"
                )
            ]
        ]
    )
    return keyboard


def create_my_tasks_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=MY_TASKS, callback_data="my_tasks")
            ]
        ]
    )
    return keyboard


def create_tasks_keyboard() -> ReplyKeyboardMarkup:
    """Формирует клавиатуру со списком заданий."""
    tasks_list_buttons = [
        [KeyboardButton(text=f"{TASKS_BUTTON_TEXT} {i + 1}")]
        for i in range(TASKS_NUMBER)
    ] + [CANCEL_BUTTON]
    return ReplyKeyboardMarkup(
        keyboard=tasks_list_buttons, resize_keyboard=True, one_time_keyboard=True
    )
