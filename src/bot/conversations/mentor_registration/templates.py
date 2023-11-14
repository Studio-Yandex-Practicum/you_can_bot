MAIN_MENTOR_USERNAME = "@katerina_bril"
ASK_FIRST_NAME = (
    "Добрый день! Для регистрации мне нужно больше узнать о Вас. Какое у Вас имя?"
)
ASK_LAST_NAME = "Отлично! Какая у Вас фамилия?"
REGISTRATION_END = (
    "Спасибо! Держите данные для входа.\n"
    "Логин: <code>{login}</code>\n"
    "Пароль: <code>{password}</code>\n"
    f"Для успешной регистрации требуется подтверждение {MAIN_MENTOR_USERNAME}. "
    "После входа обязательно смените пароль.\n\n"
    "Не блокируйте данного бота, т.к. именно он будет отправлять "
    "Вам уведомления по прикреплённым к вам подросткам."
)
CONFIRMATION_REQUEST = (
    "Добрый день! Нужно подтвердить регистрацию психолога. "
    "Будьте внимательны! После подтверждения регистрации "
    "пользователь будет иметь доступ к административной части YouCanBot.\n"
    "Имя: {first_name}\n"
    "Фамилия: {last_name}\n"
    "username: @{username}"
)
CONFIRM_BUTTON = "- Подтвердить ✅"
REJECT_BUTTON = "- Отклонить ❌"
CONFIRMED = "Регистрация одобрена ✅"
REJECTED = "Регистрация отклонена ❌"
REG_STATUS_NOT_CONFIRMED = f"Ждём подтвеждение от {MAIN_MENTOR_USERNAME}, подождите :)"
REG_STATUS_CONFIRMED = "Вы уже зарегистрированы :)"
SHORT_MSG = "Длина {} должна быть не меньше двух символов. Повторите ввод."
SHORT_FIRST_NAME_MSG = SHORT_MSG.format("имени")
SHORT_LAST_NAME_MSG = SHORT_MSG.format("фамилии")
LONG_FIRST_NAME_MSG = "Слишком длинное имя. Повторите ввод."
LONG_LAST_NAME_MSG = "Слишком длинная фамилия. Повторите ввод."
REGISTRATION_CANCEL = "Регистрация прервана."
