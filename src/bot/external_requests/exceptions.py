class PostAPIError(Exception):
    """Ошибка в ответе сервера."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class TelegramIdError(Exception):
    """Некорректный телеграм id."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class APIDataError(PostAPIError):
    """Ошибка в данных ответа сервера."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class APIForbiddenError(PostAPIError):
    """Ошибка 403 в ответе сервера."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class UserNotFound(PostAPIError):
    """Ошибка 404 в ответе сервера."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
