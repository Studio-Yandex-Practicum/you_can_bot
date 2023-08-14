from telegram import (
    BotCommand, Bot, InlineKeyboardMarkup, InlineKeyboardButton)

from . templates import (
    COMMANDS, TASKS_BUTTON_TEXT, TASKS_BUTTON_CALLBACK, TASKS_NUMBER,
    MOVE_BACK_TEXT, MOVE_BACK_CALLBACK, EDIT_PROFILE_TEXT,
    EDIT_PROFILE_CALLBACK, URL, URL_BUTTON_TEXT, CONFIRM, CANCEL,
    CONFIRM_CALLBACK, CANCEL_CALLBACK
)


MOVE_BACK_BUTTON = [
    [InlineKeyboardButton(
        text=MOVE_BACK_TEXT,
        callback_data=MOVE_BACK_CALLBACK
    )]
]

PROFILE_MENU_BUTTONS = [
    [InlineKeyboardButton(
        text=EDIT_PROFILE_TEXT, callback_data=EDIT_PROFILE_CALLBACK
    )]
] + MOVE_BACK_BUTTON

CONFIRMATION_BUTTONS = [
    [InlineKeyboardButton(
        text=CONFIRM, callback_data=CONFIRM_CALLBACK
    )],
    [InlineKeyboardButton(
        text=CANCEL, callback_data=CANCEL_CALLBACK
    )]
]

URL_BUTTON = [
    [InlineKeyboardButton(
        text=URL_BUTTON_TEXT, url=URL
    )]
]


async def create_main_menu(bot: Bot) -> None:
    """Создает кнопку с меню бота и добавляет в нее команды."""
    commands = [
        BotCommand(cmd, description) for cmd, description in COMMANDS.items()
    ]
    await bot.set_my_commands(commands=commands)


def create_tasks_keyboard(prefix: str) -> InlineKeyboardMarkup:
    """Формирует клавиатуру со списком заданий."""
    tasks_list_buttons = [
        [
            InlineKeyboardButton(
                text=f'{TASKS_BUTTON_TEXT} {i+1}',
                callback_data=f'{prefix}_{TASKS_BUTTON_CALLBACK}_{i+1}'
            )
        ] for i in range(TASKS_NUMBER)
    ] + MOVE_BACK_BUTTON
    return InlineKeyboardMarkup(tasks_list_buttons)
