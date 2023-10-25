from typing import Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .constants import (
    MAX_BUTTON_NUMBER,
    MAX_TELEGRAM_ROW_LENGTH
)


def get_default_inline_keyboard(
    button_labels: Tuple[str],
    picked_choices: str = ""
) -> InlineKeyboardMarkup:
    """
    Формирует клавиатуру, принимая на вход кортеж кнопок. При формировании
    учитывает уже выбранные пользователем ответы, исключая такие кнопки
    из клавиатуры (за исключение ответственен аргумент picked_choices, по
    умолчанию он является пустой строкой, не влияющей на формирование).
    По ограничению Telegram, количество кнопок в одном ряду клавиатуры
    не должно превышать 8, поэтому прописано ограничение MAX_BUTTON_NUMBER.
    Если количество кнопок превышает 8, то кнопки ставятся в ряды,
    содержащие MAX_BUTTON_NUMBER. Выходящие за ограничение кнопки
    переносятся на следующий ряд.
    """
    keyboard = []
    row = []
    for label in button_labels:
        if label not in picked_choices:
            button = InlineKeyboardButton(label, callback_data=label)
            row.append(button)
        if (
            len(row) == MAX_BUTTON_NUMBER
            and len(button_labels) > MAX_TELEGRAM_ROW_LENGTH
        ):
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)
