from telegram import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
)

import conversations.menu.templates as templates
from internal_requests.entities import TaskStatus

ROBOTGURU_RU_DOMAIN = "robotguru.ru"
YOUCAN_BY_DOMAIN = "youcan.by"

INFO_URL_KEYBOARD = InlineKeyboardMarkup.from_column(
    [
        InlineKeyboardButton(
            text=f"🇧🇾 {YOUCAN_BY_DOMAIN}", url=f"https://{YOUCAN_BY_DOMAIN}/"
        ),
        InlineKeyboardButton(
            text=f"🇷🇺 {ROBOTGURU_RU_DOMAIN}", url=f"https://{ROBOTGURU_RU_DOMAIN}/"
        ),
    ]
)

CANCEL_BUTTON = [KeyboardButton(text=templates.CANCEL)]
AGREE_OR_CANCEL_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Подтвердить", callback_data="agree_question"),
            InlineKeyboardButton(text="Отмена", callback_data="cancel_question"),
        ]
    ]
)

CONFIRMATION_BUTTONS = [[KeyboardButton(text=templates.CONFIRM)], CANCEL_BUTTON]


def get_main_menu_commands() -> list[BotCommand]:
    """Создает кнопку с меню бота и добавляет в нее команды."""
    return [
        BotCommand(cmd, description) for cmd, description in templates.COMMANDS.items()
    ]


def create_inline_tasks_keyboard(task_statuses: list[TaskStatus]):
    """Создает инлайн клавиатуру со списком заданий."""
    tasks_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=(
                        f"{'✅' if task.is_done else '❌'} {task.number}. {task.name}"
                    ),
                    callback_data=(
                        (
                            templates.PATTERN_DONE
                            if task.is_done
                            else templates.PATTERN_UNDONE
                        )
                        + str(task.number)
                    ),
                )
            ]
            for task in task_statuses
        ]
    )
    return tasks_keyboard
