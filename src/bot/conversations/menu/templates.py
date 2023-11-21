# Main menu button commands
COMMANDS = {
    "tasks": "Посмотреть все задания",
    "ask": "Задать вопрос",
    "info": "Перейти на сайт/инфо",
    "cancel": "Приостановить выполнение задания",
}
USER_NOT_FOUND = (
    "Я с тобой еще не знаком, поэтому не могу выполнить для тебя эту команду. "
    "Если хочешь познакомиться, введи команду /start"
)

# Profile
SHOW_MY_TASKS_STATE = "SHOW_MY_TASKS"
USER_PROFILE_TEXT = "<b>Имя:</b> {name}\n" "<b>Фамилия:</b> {surname}\n"
TASKS_LIST_TEXT = (
    "Нажав на кнопку с заданием, ты можешь начать, или продолжить его выполнение, "
    "или посмотреть результаты."
)
NAME_PATTERN = "^[A-Za-zА-яЁё ]+$"

# Show all tasks + show user results
TASKS_STATE = "TASKS"
MY_TASKS = "Мои задания"
TASKS_BUTTON_TEXT = "Задание"
PATTERN_DONE = "result_task_"
PATTERN_UNDONE = "with_choice_start_task_"
PICKED_TASK = "<b>Выбранное задание: {task_number}</b>"

# Ask question
WAITING_FOR_QUESTION_STATE = "WAITING_FOR_QUESTION"
ASK_ME_QUESTION_TEXT = "Отправь вопрос, который тебя интересует."
SEND_QUESTION_TEXT = "Подтверди отправку вопроса психологу."
QUESTION_CONFIRMATION_TEXT = (
    "Твой вопрос был сохранен. " "Чуть позже тебе ответит психолог."
)
QUESTION_CANCEL = "Вопрос не отправлен, но это можно сделать позднее."

# Get more info
GET_MORE_INFO_TEXT = "Узнай больше на сайте YOU CAN"
URL_BUTTON_TEXT = "Перейти на сайт"
URL = "https://youcan.by/"

CONFIRM = "Подтвердить"
CANCEL = "Отменить"

YOUR_ANSWER = "Твой ответ:\n\n{}"
YOUR_ANSWERS = "Твои ответы:\n\n{}"
