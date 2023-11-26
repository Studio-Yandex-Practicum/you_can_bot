# Main menu button commands
COMMANDS = {
    "tasks": "Посмотреть все задания",
    "ask": "Задать вопрос",
    "info": "Перейти на сайт/инфо",
}
USER_NOT_FOUND = (
    "Я с тобой еще не знаком, поэтому не могу выполнить для тебя эту команду. "
    "Если хочешь познакомиться, введи команду /start"
)

# Show all tasks + show user results
TASKS_STATE = "TASKS"
TASKS_BUTTON_TEXT = "Задание"
PATTERN_DONE = "result_task_"
PATTERN_UNDONE = "with_choice_start_task_"
PICKED_TASK = "<b>Выбранное задание: {task_number}</b>"
TASKS_LIST_TEXT = (
    "Нажав на кнопку с заданием, ты можешь начать, или продолжить его выполнение, "
    "или посмотреть результаты."
)

# Ask question
WAITING_FOR_QUESTION_STATE = "WAITING_FOR_QUESTION"
WAITING_FOR_CONFIRMATION_STATE = "WAITING_FOR_CONFIRMATION"
ASK_ME_QUESTION_TEXT = "Отправь вопрос, который тебя интересует."
SEND_QUESTION_TEXT = (
    "После подтверждения этот вопрос будет отправлен профдизайнеру."
    " До подтверждения ты можешь его изменить.\n\n<b>Текущий вопрос:</b> "
)
QUESTION_CONFIRMATION_TEXT = (
    "Твой вопрос был сохранен. Чуть позже тебе ответит профдизайнер."
)
QUESTION_CANCEL = (
    "Хорошо, вопрос не отправлен."
    " Но ты можешь попробовать снова в любое время, просто вызови команду /ask."
)

# Get more info
GET_MORE_INFO_TEXT = "Узнай больше на сайте YOU CAN"
URL_BUTTON_TEXT = "Перейти на сайт"
URL = "https://youcan.by/"

CONFIRM = "Подтвердить"
CANCEL = "Отменить"
