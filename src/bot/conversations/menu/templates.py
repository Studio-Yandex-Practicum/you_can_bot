# Main menu button commands
COMMANDS = {
    "tasks": "Посмотреть задания",
    "ask": "Задать вопрос",
    "info": "Перейти на сайт",
    "cancel": "Завершить текущую команду",
}
USER_NOT_FOUND = (
    "Я с тобой еще не знаком, поэтому не могу выполнить для тебя эту команду. "
    "Если хочешь познакомиться, введи команду /start"
)

# Show all tasks + show user results
TASKS_STATE = "TASKS"
TASKS_BUTTON_TEXT = "Задание"
PATTERN_DONE = "result_task_"
PATTERN_UNDONE = "start_task_from_command_"
TASKS_LIST_TEXT = (
    "Нажав на кнопку с заданием, ты можешь начать, или продолжить его выполнение,"
    " или посмотреть результаты."
)

# Ask question
WAITING_FOR_QUESTION_STATE = "WAITING_FOR_QUESTION"
WAITING_FOR_CONFIRMATION_STATE = "WAITING_FOR_CONFIRMATION"
ASK_ME_QUESTION_TEXT = "Отправь вопрос, который тебя интересует."
SEND_QUESTION_TEXT = (
    "После подтверждения вопрос будет отправлен."
    " До подтверждения ты можешь его изменить.\n\n<b>Текущий вопрос:</b> "
)
QUESTION_CONFIRMATION_TEXT = (
    "<b>Твой вопрос отправлен.</b>\n\n" "В течение 48 часов тебе ответит профдизайнер."
)
QUESTION_CANCEL = (
    "<b>Твой вопрос не отправлен.</b>\n\n"
    "Если надумаешь отправить вопрос, вызови команду /ask."
)

# Get more info
GET_MORE_INFO_TEXT = (
    "Узнай больше о проекте — переходи на сайт, нажав одну из кнопок ниже."
    " Контент для Беларуси и России отличается, поэтому выбирай свою страну:"
)

CONFIRM = "Подтвердить"
CANCEL = "Отменить"
