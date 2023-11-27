from telegram import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
)

import conversations.menu.templates as templates

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

URL_BUTTON = InlineKeyboardMarkup.from_button(
    InlineKeyboardButton(text=templates.URL_BUTTON_TEXT, url=templates.URL)
)


def get_main_menu_commands() -> list[BotCommand]:
    """Создает кнопку с меню бота и добавляет в нее команды."""
    return [
        BotCommand(cmd, description) for cmd, description in templates.COMMANDS.items()
    ]


def create_inline_tasks_keyboard(tasks):
    """Создает инлайн клавиатуру со списком заданий."""
    tasks_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=(
                        f"{'✅' if info.is_done else '❌'} "
                        f"{templates.TASKS_BUTTON_TEXT + ' ' + str(info.number)}"
                    ),
                    callback_data=(
                        (
                            templates.PATTERN_DONE
                            if info.is_done
                            else templates.PATTERN_UNDONE
                        )
                        + str(info.number)
                    ),
                )
            ]
            for info in tasks
        ]
    )
    return tasks_keyboard
