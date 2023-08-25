from rest_framework.test import APITestCase

from api.models import UserFromTelegram


class BaseCaseForTests(APITestCase):
    """Базовый набор констант для тестов модуля api."""

    TELEGRAM_ID = 1234567
    TELEGRAM_USERNAME = "hasnoname"
    TELEGRAM_NAME = "HasNoName"
    TELEGRAM_SURNAME = "HasNoSurname"
    CONTENT_TYPE_JSON = "application/json"
    TASK_NUMBER_1 = 1
    TASK_NUMBER_99 = 99
    ANSWER_1 = {"number": "1", "content": "a"}
    ANSWER_2 = {"number": 1, "content": "б"}
    ANSWER_3 = {"number": "first", "content": "б"}
    ANSWER_4 = {"number": 2, "content": "a"}
    ANSWER_5 = {"number": 1}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_from_telegram = UserFromTelegram.objects.create(
            telegram_id=cls.TELEGRAM_ID,
            telegram_username=cls.TELEGRAM_USERNAME,
            name=cls.TELEGRAM_NAME,
            surname=cls.TELEGRAM_SURNAME,
        )
