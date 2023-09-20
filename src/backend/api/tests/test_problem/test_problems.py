from django.urls import reverse
from rest_framework import status

from api.models import Problem
from api.tests.test_problem.fixtures import BaseCaseForProblemTests


class ProblemTests(BaseCaseForProblemTests):
    """
    Проверка работы эндпоинта api/v1/users/{telegram_id}/problems/:
    доступность, занесение данных в БД.
    """

    def test_status_codes_problem(self):
        """
        Проверка доступности эндпоинта api/v1/users/{telegram_id}/problems/
        для метода POST (метод OPTIONS включен по умолчанию).
        """
        common_url = reverse(
            "api:problem_create",
            kwargs={"telegram_id": self.TELEGRAM_ID},
        )

        response = self.client.get(common_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.assertIn('Allow', response)
        self.assertEqual(response['Allow'], 'POST, OPTIONS')

    def test_db_problem(self):
        """
        Проверка занесения данных в таблицу Problems.
        """
        url = reverse(
            "api:problem_create",
            kwargs={"telegram_id": self.TELEGRAM_ID},
        )
        self.assertEqual(
            Problem.objects.filter(
                message=self.MESSAGE,
            ).exists(),
            False,
        )
        response = self.client.post(url, data={"message": self.MESSAGE})
        self.assertEqual(
            Problem.objects.filter(
                message=self.MESSAGE,
            ).exists(),
            True,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_problem_from_unknown_user(self):
        """
        Проверка доступности эндпоинта api/v1/users/{telegram_id}/problems/
        для неизвестного пользователя.
        """
        url = reverse(
            "api:problem_create",
            kwargs={"telegram_id": self.UNKNOWN_USER_TELEGRAM_ID},
        )
        response = self.client.post(url, data={"message": self.MESSAGE})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
