from rest_framework.test import APITestCase

from api.models import UserFromTelegram


class BaseCaseForProblemTests(APITestCase):
    """Базовый набор констант для тестов модуля api."""

    TELEGRAM_ID = 1234567
    UNKNOWN_USER_TELEGRAM_ID = 7654321
    TELEGRAM_USERNAME = "hasnoname"
    TELEGRAM_NAME = "HasNoName"
    TELEGRAM_SURNAME = "HasNoSurname"
    CONTENT_TYPE_JSON = "application/json"
    MESSAGE = "Как дела?"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_from_telegram = UserFromTelegram.objects.create(
            telegram_id=cls.TELEGRAM_ID,
            telegram_username=cls.TELEGRAM_USERNAME,
            name=cls.TELEGRAM_NAME,
            surname=cls.TELEGRAM_SURNAME,
        )
