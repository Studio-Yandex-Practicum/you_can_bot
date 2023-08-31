from django.urls import reverse
from rest_framework import status

from api.tests.test_case import BaseCaseForAnswerTests


class UrlAnswerTests(BaseCaseForAnswerTests):
    """Проверка url модуля api."""

    def test_status_codes_answer_create(self):
        """Проверка кодов возврата: answer_create."""
        common_url = reverse(
            "api:answer_create",
            kwargs={"telegram_id": self.TELEGRAM_ID, "task_number": self.TASK_NUMBER_1},
        )
        status_codes = [
            [common_url, status.HTTP_201_CREATED],
            [
                reverse(
                    "api:answer_create",
                    kwargs={
                        "telegram_id": self.TELEGRAM_ID,
                        "task_number": self.TASK_NUMBER_99,
                    },
                ),
                status.HTTP_404_NOT_FOUND,
            ],
        ]
        for url, expected_status in status_codes:
            self.assertEqual(
                self.client.post(url, data=self.ANSWER_1).status_code, expected_status
            )

        status_codes = [
            [self.ANSWER_2, status.HTTP_201_CREATED],
            [self.ANSWER_2, status.HTTP_201_CREATED],
            [self.ANSWER_3, status.HTTP_400_BAD_REQUEST],
            [self.ANSWER_4, status.HTTP_201_CREATED],
            [self.ANSWER_5, status.HTTP_400_BAD_REQUEST],
        ]
        for data, expected_status in status_codes:
            self.assertEqual(
                self.client.post(common_url, data=data).status_code, expected_status
            )

    def test_answerbody_answer_create(self):
        """Проверка содержания возвращаемых ответов: answer_create."""
        common_url = reverse(
            "api:answer_create",
            kwargs={"telegram_id": self.TELEGRAM_ID, "task_number": self.TASK_NUMBER_1},
        )

        response = self.client.post(common_url, data=self.ANSWER_1)
        self.assertEqual(response.data["number"], int(self.ANSWER_1["number"]))
        self.assertEqual(response.data["content"], self.ANSWER_1["content"])
        self.assertEqual(response.get("task"), None)
        answer_id = response.data["id"]

        response = self.client.post(common_url, data=self.ANSWER_2)
        self.assertEqual(response.data["number"], self.ANSWER_2["number"])
        self.assertEqual(response.data["content"], self.ANSWER_2["content"])
        self.assertEqual(response.data["id"], answer_id)

        response = self.client.post(common_url, data=self.ANSWER_2)
        self.assertEqual(response.data["number"], int(self.ANSWER_2["number"]))
        self.assertEqual(response.data["content"], self.ANSWER_2["content"])
        self.assertEqual(response.data["id"], answer_id)

        response = self.client.post(common_url, data=self.ANSWER_4)
        self.assertEqual(response.data["number"], self.ANSWER_4["number"])
        self.assertEqual(response.data["content"], self.ANSWER_4["content"])
        self.assertNotEqual(response.data["id"], answer_id)
