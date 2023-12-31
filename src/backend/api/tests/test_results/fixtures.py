from django.urls import reverse
from rest_framework.test import APITestCase

from api.models import Result, ResultStatus, TaskStatus, UserFromTelegram


class BaseCaseForResultsTests(APITestCase):
    """Базовый набор констант для тестов получения результата по
    конкретному заданию для пользователя."""

    TELEGRAM_ID = 1234567
    INCORRECT_TELEGRAM_ID = 12345
    TELEGRAM_USERNAME = "test_username"
    TELEGRAM_NAME = "test_name"
    TELEGRAM_SURNAME = "test_surname"
    RESULT_KEY = "test_key"
    RESULT_TITLE = "test_title"
    RESULT_DESCRIPTION = "test_description"
    TASK_STATUS_IS_DONE = False
    RESULT_STATUS_TOP = 1
    RESULT_STATUS_SCORE = 10
    TASK_NUMBER_1 = 1
    TASK_NUMBER_99 = 99
    TASK_STATUS_ID = 1
    URL_NAME = "api:get_results_for_user_by_task"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_from_telegram = UserFromTelegram.objects.create(
            telegram_id=cls.TELEGRAM_ID,
            telegram_username=cls.TELEGRAM_USERNAME,
            name=cls.TELEGRAM_NAME,
            surname=cls.TELEGRAM_SURNAME,
        )
        cls.task_status = TaskStatus.objects.get(
            user_id=cls.user_from_telegram.id, task_id=cls.TASK_NUMBER_1
        )
        cls.task_status.is_done = True
        cls.task_status.save()

        cls.result = Result.objects.create(
            task_id=cls.TASK_NUMBER_1,
            key=cls.RESULT_KEY,
            title=cls.RESULT_TITLE,
            description=cls.RESULT_DESCRIPTION,
        )
        cls.result_status = ResultStatus.objects.create(
            task_status_id=cls.TASK_STATUS_ID,
            top=cls.RESULT_STATUS_TOP,
            result_id=cls.result.id,
            score=cls.RESULT_STATUS_SCORE,
        )
        cls.data = {
            "correct": reverse(
                cls.URL_NAME,
                kwargs={
                    "telegram_id": cls.TELEGRAM_ID,
                    "task_number": cls.TASK_NUMBER_1,
                },
            ),
            "incorrect_user": reverse(
                cls.URL_NAME,
                kwargs={
                    "telegram_id": cls.INCORRECT_TELEGRAM_ID,
                    "task_number": cls.TASK_NUMBER_1,
                },
            ),
            "incorrect_task": reverse(
                cls.URL_NAME,
                kwargs={
                    "telegram_id": cls.TELEGRAM_ID,
                    "task_number": cls.TASK_NUMBER_99,
                },
            ),
        }
