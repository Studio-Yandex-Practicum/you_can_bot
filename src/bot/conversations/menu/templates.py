# Main menu button commands
COMMANDS = {
    "profile": "Профиль",
    "tasks": "Посмотреть все задания",
    "ask": "Задать вопрос",
    "info": "Перейти на сайт/инфо",
}

# Profile
USER_PROFILE_TEXT = "<b>Имя:</b> {name}\n" "<b>Фамилия:</b> {surname}\n"
MY_TASKS_START = 1
TASKS_LIST_TEXT = (
    "Нажав на кнопку с заданием, ты можешь начать, или продолжить его выполнение, "
    "или посмотреть результаты."
)
EDIT_PROFILE_TEXT = "Редактировать профиль"
EDIT_PROFILE, WAITING_FOR_NAME, WAITING_FOR_SURNAME = range(3)
ENTER_NAME = "Введи свое имя.\n" "Допустимы буквы русского и латинского алфавитов."
ENTER_SURNAME = (
    "Отлично! А теперь введи свою фамилию.\n"
    "Допустимы буквы русского и латинского алфавитов."
)
CONFIRM_PROFILE_CHANGING = "Сохранить изменения в профиле?"
INCORRECT_NAME = (
    "Возникла ошибка. Повтори ввод. "
    "Допустимы только буквы русского "
    "или латинского алфавита"
)
PROFILE_CHANGED = "Изменения сохранены"
NAME_PATTERN = "^[A-Za-zА-яЁё ]+$"

# Show all tasks + show user results
SHOW_TASKS = 1
MY_TASKS = "Мои задания"
TASKS_NUMBER = 8
TASKS_BUTTON_TEXT = "Задание"
TASK_RESULTS = 1
PATTERN_DONE = "result_task_"
PATTERN_UNDONE = "start_task_"
PICKED_TASK = "<b>Выбранное задание: {task_number}</b>"

# Ask question
ASK_ME_QUESTION_TEXT = "Отправь вопрос, который тебя интересует."
WAITING_FOR_QUESTION = 0
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
