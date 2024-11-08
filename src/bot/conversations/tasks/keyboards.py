from typing import Tuple, Union

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from conversations.tasks.constants import MAX_BUTTON_NUMBER, MAX_TELEGRAM_ROW_LENGTH

BUTTON_LABELS_PATTERN = r"^([1-9]|10|[А-Е])$"
NEXT_BUTTON_PATTERN = r"^Далее$"
SHOW_RESULTS_BUTTON_PATTERN = r"^show_results$"
CONFIRM_BUTTON_PATTERN = r"^confirm_answer$"
TASK_START_BUTTON_LABEL = "Задание "

CHOICES_SIX_LETTERS = ("А", "Б", "В", "Г", "Д", "Е")
CHOICES_TWO_LETTERS = ("А", "Б")
CHOICES_TEN_NUMBERS = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")

CONFIRM_KEYBOARD = InlineKeyboardMarkup(
    ((InlineKeyboardButton(text="Подтвердить", callback_data="confirm_answer"),),)
)

NEXT_KEYBOARD = InlineKeyboardMarkup(
    ((InlineKeyboardButton(text="Далее", callback_data="Далее"),),)
)

SHOW_RESULTS_BUTTON = InlineKeyboardMarkup.from_button(
    InlineKeyboardButton(text="Посмотреть результаты", callback_data="show_results")
)


def get_default_inline_keyboard(
    button_labels: Union[Tuple[str], str], picked_choices: str = ""
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
