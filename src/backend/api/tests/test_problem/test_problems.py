from unittest.mock import patch

from django.urls import reverse
from rest_framework import status

from api.models import Problem
from api.tests.test_problem.fixtures import BaseCaseForProblemTests
from api.views.problems import PROBLEM_TEXT


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

        self.assertIn("Allow", response)

        allowed_methods = response["Allow"]
        allowed_methods_list = [method.strip() for method in allowed_methods.split(",")]
        self.assertIn("POST", allowed_methods_list)
        self.assertIn("OPTIONS", allowed_methods_list)

    @patch("api.views.problems.non_context_send_message")
    def test_db_problem(self, mock_send_message):
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
        self.assertEqual(mock_send_message.called, True)
        mock_send_message.assert_called_with(
            text=PROBLEM_TEXT.format(
                question=self.MESSAGE,
                user=(
                    f"{self.user_from_telegram.name}"
                    f" {self.user_from_telegram.surname}"
                ),
            ),
            user_id=self.MENTOR_TELEGRAM_ID,
        )

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

    def test_message_field_is_required(self):
        """
        Проверка, что message - обязательное поле.
        """
        EMPTY_FIELD_MSG = "message - обязательное поле."

        url = reverse(
            "api:problem_create",
            kwargs={"telegram_id": self.TELEGRAM_ID},
        )

        response = self.client.post(url, data={"message": self.EMPTY_MESSAGE_1})
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, EMPTY_FIELD_MSG
        )

        response = self.client.post(url, data={"message": self.EMPTY_MESSAGE_2})
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, EMPTY_FIELD_MSG
        )

        response = self.client.post(url)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, EMPTY_FIELD_MSG
        )
