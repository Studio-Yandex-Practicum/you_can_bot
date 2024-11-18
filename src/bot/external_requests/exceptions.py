class TelegramIdError(Exception):
    """Исключение при получении некорректного значения Chat ID."""

    pass


class UserNotFound(Exception):
    """Исключение при статусе 404 в ответах от API личных кабинетов."""

    pass


class ValidationExternalResponseError(Exception):
    """Исключение, если полученные от личного кабинета данные невалидны."""

    pass
