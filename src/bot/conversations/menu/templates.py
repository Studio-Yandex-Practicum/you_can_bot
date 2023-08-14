# Main menu button commands
COMMANDS = {
    'profile': 'Профиль',
    'all_tasks': 'Посмотреть все задания',
    'my_results': 'Посмотреть расшифровку моих заданий',
    'ask': 'Задать вопрос',
    'info': 'Перейти на сайт/инфо',
}

# Profile
USER_PROFILE_TEXT = (
    'Имя: {name}\n'
    'Пройдено заданий: {tasks_completed}\n'
)
EDIT_PROFILE_TEXT = 'Редактировать профиль'
EDIT_PROFILE_CALLBACK = 'EDIT_PROFILE'
EDIT_PROFILE, WAITING_FOR_NAME = range(2)
ENTER_NAME = ('Введи свое имя.\n'
              'Допустимы буквы русского и латинского алфавитов.')
NEW_NAME = 'Новое имя - {user_name}. Сохранить изменения?'
INCORRECT_NAME = ('Возникла ошибка. Введи имя заново. '
                  'Оно должно состоять из букв '
                  'русского или латинского алфавита')
NAME_CHANGED = 'Изменения сохранены'

# All tasks + My results
TASKS_LIST_TEXT = 'Выбери задание'
TASKS_NUMBER = 8
TASKS_BUTTON_TEXT = 'Задание'
TASKS_BUTTON_CALLBACK = 'TASK'
MOVE_BACK_TEXT = 'Назад'
MOVE_BACK_CALLBACK = 'MOVE_BACK'
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
CONFIRM_CALLBACK = 'CONFIRM'
CANCEL = 'Отменить'
CANCEL_CALLBACK = 'CANCEL'
CANCEL_TEXT = 'Изменения отменены'

# Temporary (to be removed when get data from data base)
GET_NUMBER_FROM_DB = 10
