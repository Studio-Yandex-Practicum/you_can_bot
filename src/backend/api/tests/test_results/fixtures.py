from rest_framework.test import APITestCase
from django.urls import reverse
from api.models import UserFromTelegram, ResultStatus, Result


class BaseCaseForResultsTests(APITestCase):
    """Базовый набор констант для тестов получения результата по
    конкретному заданию для пользователя."""

    TELEGRAM_ID = 1234567
    TELEGRAM_USERNAME = "test_username"
    TELEGRAM_NAME = "test_name"
    TELEGRAM_SURNAME = "test_surname"
    RESULT_KEY = "test_key"
    RESULT_TITLE = "test_title"
    RESULT_DESCRIPTION = "test_description"
    TASK_STATUS_IS_DONE = False
    TASK_STATUS_CURRENT_QUESTION = 1
    RESULT_STATUS_TOP = 1
    RESULT_STATUS_SCORE = 10
    TASK_NUMBER_1 = 1
    TASK_NUMBER_99 = 99
    RESULT_STATUS_TASK_STATUS_ID = 1

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_from_telegram = UserFromTelegram.objects.create(
            telegram_id=cls.TELEGRAM_ID,
            telegram_username=cls.TELEGRAM_USERNAME,
            name=cls.TELEGRAM_NAME,
            surname=cls.TELEGRAM_SURNAME,
        )
        cls.result = Result.objects.create(
            task_id=cls.TASK_NUMBER_1,
            key=cls.RESULT_KEY,
            title=cls.RESULT_TITLE,
            description=cls.RESULT_DESCRIPTION,
        )
        ResultStatus.objects.create(
            task_status_id=cls.RESULT_STATUS_TASK_STATUS_ID,
            top=cls.RESULT_STATUS_TOP,
            result_id=cls.result.id,
            score=cls.RESULT_STATUS_SCORE,
        )
