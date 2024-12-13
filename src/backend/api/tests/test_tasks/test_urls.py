from django.urls import reverse
from rest_framework import status

from api.tests.test_answer.fixtures import BaseCaseForAnswerTests


class UrlTasksTests(BaseCaseForAnswerTests):
    """Проверка url модуля tasks."""

    WRONG_TELEGRAM_ID = 222222

    def test_status_codes_tasks(self):
        """Проверка кодов возврата: tasks."""
        common_url = reverse(
            "api:user-tasks-list",
            kwargs={"telegram_id": self.TELEGRAM_ID},
        )
        first_task_url = reverse(
            "api:user-tasks-detail",
            kwargs={
                "telegram_id": self.TELEGRAM_ID,
                "task__number": self.TASK_NUMBER_1,
            },
        )
        nonexistent_task_url = reverse(
            "api:user-tasks-detail",
            kwargs={
                "telegram_id": self.TELEGRAM_ID,
                "task__number": self.TASK_NUMBER_99,
            },
        )
        nonexistent_user_url = reverse(
            "api:user-tasks-list",
            kwargs={"telegram_id": self.WRONG_TELEGRAM_ID},
        )
        status_codes = [
            [common_url, status.HTTP_200_OK],
            [first_task_url, status.HTTP_200_OK],
            [nonexistent_task_url, status.HTTP_404_NOT_FOUND],
            [nonexistent_user_url, status.HTTP_404_NOT_FOUND],
        ]
        for url, expected_status in status_codes:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, expected_status)
