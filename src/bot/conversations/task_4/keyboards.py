from telegram import ReplyKeyboardMarkup


TEXT_ENTRY_POINT_BUTTON_FOR_TASK_4 = "ЗАДАНИЕ 4"
CANCEL_COMMAND = "cancel"
NEXT = "ДАЛЕЕ"
NEXT_PLACEHOLDER = f"Жми смело кнопку {NEXT}"
NEXT_KEYBOARD = [[NEXT]]
INPUT_PLACEHOLDER = "1 не согласен...10 согласен"
ANSWER = "Ответ пользователя %s на %s вопрос: %s"
CANSEL = "Пользователь %s закончил диалог."
BUTTONS = {
    1: '1\uFE0F\u20E3',
    2: '2\uFE0F\u20E3',
    3: '3\uFE0F\u20E3',
    4: '4\uFE0F\u20E3',
    5: '5\uFE0F\u20E3',
    6: '6\uFE0F\u20E3',
    7: '7\uFE0F\u20E3',
    8: '8\uFE0F\u20E3',
    9: '9\uFE0F\u20E3',
    10: '\U0001f51f',
}
KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [BUTTONS[1], BUTTONS[2], BUTTONS[3], BUTTONS[4], BUTTONS[5]],
        [BUTTONS[6], BUTTONS[7], BUTTONS[8], BUTTONS[9], BUTTONS[10]]
    ],
    resize_keyboard=True,
    input_field_placeholder=INPUT_PLACEHOLDER,
    one_time_keyboard=True,
)
