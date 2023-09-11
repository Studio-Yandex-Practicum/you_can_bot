from api.tests.test_results.fixtures import BaseCaseForResultsTests
from django.urls import reverse
from rest_framework import status


class ResultsURLTests(BaseCaseForResultsTests):
    """Тест url."""

    def test_status_code_get_results(self):
        """Проверка доступности url."""
        response = self.client.get(
            reverse(
                "api:get_results_for_user_by_task",
                kwargs={
                    "telegram_id": self.TELEGRAM_ID,
                    "task_number": self.TASK_NUMBER_1
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_idempotency_get_results(self):
        """Проверка идемпотентности api."""
        common_url = reverse(
                "api:get_results_for_user_by_task",
                kwargs={
                    "telegram_id": self.TELEGRAM_ID,
                    "task_number": self.TASK_NUMBER_1
                },
            )
        response_1 = self.client.get(common_url)
        response_2 = self.client.get(common_url)

        self.assertEqual(response_1.content, response_2.content)