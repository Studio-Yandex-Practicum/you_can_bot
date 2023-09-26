from telegram import InlineKeyboardButton, InlineKeyboardMarkup

START_TASK_1_KEYBOARD = InlineKeyboardMarkup(
    ((InlineKeyboardButton(text="Далее", callback_data="Далее"),),)
)
GO_TO_TASK_2_KEYBOARD = InlineKeyboardMarkup(
    ((InlineKeyboardButton(text="ЗАДАНИЕ 2", callback_data="ЗАДАНИЕ 2"),),)
)


def get_inline_keyboard(buttons: str, picked_choices: str = "") -> InlineKeyboardMarkup:
    """Добавляет кнопки в сообщении с учетом уже выбранных ответов."""
    keyboard = []
    for label in buttons:
        if label not in picked_choices:
            keyboard.append(InlineKeyboardButton(label, callback_data=label))
    return InlineKeyboardMarkup([keyboard])
