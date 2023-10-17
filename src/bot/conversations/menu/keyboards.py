from telegram import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
)

from .templates import (
    CANCEL,
    COMMANDS,
    CONFIRM,
    MY_TASKS,
    PATTERN_DONE,
    PATTERN_UNDONE,
    TASKS_BUTTON_TEXT,
    URL,
    URL_BUTTON_TEXT,
)

CANCEL_BUTTON = [KeyboardButton(text=CANCEL)]

CONFIRMATION_BUTTONS = [[KeyboardButton(text=CONFIRM)], CANCEL_BUTTON]

URL_BUTTON = [[KeyboardButton(text=URL_BUTTON_TEXT, web_app=WebAppInfo(url=URL))]]


def get_main_menu_commands() -> list[BotCommand]:
    """Создает кнопку с меню бота и добавляет в нее команды."""
    return [BotCommand(cmd, description) for cmd, description in COMMANDS.items()]


def create_inline_tasks_keyboard(tasks):
    """Создает инлайн клавиатуру со списком заданий."""
    tasks_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=(
                        f"{'✅' if info.is_done else '❌'} "
                        f"{TASKS_BUTTON_TEXT + ' ' + str(info.number)}"
                    ),
                    callback_data=(
                        (PATTERN_DONE if info.is_done else PATTERN_UNDONE)
                        + str(info.number)
                    ),
                )
            ]
            for info in tasks
        ]
    )
    return tasks_keyboard


def create_inline_buttons_agree_or_cancel():
    """Создает инлайн клавиатуру со кнопками подтвердить и отменить."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Подтвердить", callback_data="agree_question"
                ),
                InlineKeyboardButton(text="Отмена", callback_data="cancel_question"),
            ]
        ]
    )
    return keyboard


def create_my_tasks_keyboard():
    """Создает инлайн клавиатуру с кнопкой мои задания."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=MY_TASKS, callback_data="my_tasks")]
        ]
    )
    return keyboard
