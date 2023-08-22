import json

from django.contrib.auth import get_user

from api.tests.test_case import BaseCaseForTests


class UrlTests(BaseCaseForTests):
    """Проверка url модуля api."""

    def test_status_codes_answer_create(self):
        """Проверка кодов возврата: answer_create."""
        common_url = self.URL_ANSWER_CREATE.format(
            telegram_id=self.TELEGRAM_ID, task_number=self.TASK_NUMBER_1
        )
        status_codes = [
            [
                common_url, self.guest_client, 201
            ],
            [
                self.URL_ANSWER_CREATE.format(
                    telegram_id=self.TELEGRAM_ID,
                    task_number=self.TASK_NUMBER_99
                ), self.guest_client, 404
            ]
        ]
        for url, client, expected_status in status_codes:
            with self.subTest(url=url, user=get_user(client)):
                self.assertEqual(
                    client.post(
                        url,
                        data=json.dumps(self.ANSWER_1),
                        content_type=self.CONTENT_TYPE_JSON
                    ).status_code, expected_status
                )
        self.assertEqual(
            self.guest_client.post(
                common_url,
                data=json.dumps(self.ANSWER_2),
                content_type=self.CONTENT_TYPE_JSON
            ).status_code, 201
        )
        self.assertEqual(
            self.guest_client.post(
                common_url,
                data=json.dumps(self.ANSWER_3),
                content_type=self.CONTENT_TYPE_JSON
            ).status_code, 201
        )
        self.assertEqual(
            self.guest_client.post(
                common_url,
                data=json.dumps(self.ANSWER_4),
                content_type=self.CONTENT_TYPE_JSON
            ).status_code, 201
        )
        self.assertEqual(
            self.guest_client.post(
                common_url,
                data=json.dumps(self.ANSWER_5),
                content_type=self.CONTENT_TYPE_JSON
            ).status_code, 400
        )

    def test_answerbody_answer_create(self):
        """Проверка кодов возврата: answer_create."""
        common_url = self.URL_ANSWER_CREATE.format(
            telegram_id=self.TELEGRAM_ID, task_number=self.TASK_NUMBER_1
        )
        response = self.guest_client.post(
            common_url, data=json.dumps(self.ANSWER_2), content_type=self.CONTENT_TYPE_JSON
        )
        print(response.content)
