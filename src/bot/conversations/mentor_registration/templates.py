MAIN_MENTOR_USERNAME = "@katerina_bril"
ASK_FIRST_NAME = (
    "Добрый день!\n\n"
    "Для регистрации в проекте в качестве профдизайнера,"
    " необходимо заполнить анкетные данные ниже.\n\n"
    "Как вас зовут?"
)
ASK_LAST_NAME = "Как ваша фамилия?"
REGISTRATION_END = (
    "Спасибо! Данные для входа.\n"
    "<b>Логин:</b> <code>{login}</code>\n"
    "<b>Пароль:</b> <code>{password}</code>\n\n"
    "<b>Важно:</b>"
    f"👉 Для входа в личный кабинет"
    f" дождитесь подтверждения от {MAIN_MENTOR_USERNAME}.\n\n"
    "👉 Во время первого входа обязательно смените пароль.\n\n"
    "❗ Не блокируйте данного бота, т.к. именно он будет"
    " отправлять вам уведомления по прикреплённым к вам подросткам."
)
CONFIRMATION_REQUEST = (
    "Добрый день!\n\nПодтвердите регистрацию профдизайнера. "
    "<b>Важно:</b> после подтверждения пользователь"
    " будет иметь доступ к административной части YouCanBot.\n\n"
    "<b>Имя:</b> {first_name}\n"
    "<b>Фамилия:</b> {last_name}\n"
    "<b>username:</b> @{username}"
)
CONFIRM_BUTTON = "Подтвердить ✅"
REJECT_BUTTON = "Отклонить ❌"
CONFIRMED = "Регистрация одобрена ✅"
REJECTED = "Регистрация отклонена ❌"
REG_STATUS_NOT_CONFIRMED = f"Ожидайте подтверждения от {MAIN_MENTOR_USERNAME}."
REG_STATUS_CONFIRMED = "Вы уже зарегистрированы ✅"
SHORT_MSG = "Длина {} должна быть не меньше двух символов. Повторите ввод."
SHORT_FIRST_NAME_MSG = SHORT_MSG.format("имени")
SHORT_LAST_NAME_MSG = SHORT_MSG.format("фамилии")
LONG_FIRST_NAME_MSG = "Слишком длинное имя. Повторите ввод."
LONG_LAST_NAME_MSG = "Слишком длинная фамилия. Повторите ввод."
REGISTRATION_CANCEL = "Регистрация прервана."
