# Main menu button commands
COMMANDS = {
    'profile': 'Профиль',
    'tasks': 'Посмотреть все задания',
    'results': 'Посмотреть расшифровку моих заданий',
    'ask': 'Задать вопрос',
    'info': 'Перейти на сайт/инфо',
}

# Profile
USER_PROFILE_TEXT = (
    'Имя: {name}\n'
    'Пройдено заданий: {tasks_completed}\n'
)
EDIT_PROFILE_TEXT = 'Редактировать профиль'
EDIT_PROFILE, WAITING_FOR_NAME, WAITING_FOR_SURNAME = range(3)
ENTER_NAME = ('Введи свое имя.\n'
              'Допустимы буквы русского и латинского алфавитов.')
ENTER_SURNAME = ('Отлично! А теперь введи свою фамилию.\n'
                 'Допустимы буквы русского и латинского алфавитов.')
CONFIRM_PROFILE_CHANGING = 'Сохранить изменения в профиле?'
INCORRECT_NAME = ('Возникла ошибка. Повтори ввод. '
                  'Допустимы только буквы русского '
                  'или латинского алфавита')
PROFILE_CHANGED = 'Изменения сохранены'

# Show all tasks + show user results
TASKS_LIST_TEXT = 'Выбери задание'
TASKS_NUMBER = 8
TASKS_BUTTON_TEXT = 'Задание'
MOVE_BACK_TEXT = 'Назад'
MOVE_BACK_MSG = 'Нажми меню для начала работы'

# Ask question
ASK_ME_QUESTION_TEXT = 'Задай вопрос, который тебя интересует'
WAITING_FOR_QUESTION = 0
SEND_QUESTION_TEXT = 'Подтверди отправку вопроса специалисту'
QUESTION_CONFIRMATION_TEXT = ('Твой вопрос был сохранен. '
                              'Чуть позже тебе ответит специалист.')

# Get more info
GET_MORE_INFO_TEXT = 'Узнай больше на сайте YOU CAN'
URL_BUTTON_TEXT = 'Перейти на сайт'
URL = 'https://youcan.by/'


CONFIRM = 'Подтвердить'
CANCEL = 'Отменить'
CANCEL_TEXT = 'Изменения отменены'

# Temporary (to be removed when get data from data base)
GET_NUMBER_FROM_DB = 5
