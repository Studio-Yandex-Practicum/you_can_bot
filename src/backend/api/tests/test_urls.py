import json

from django.contrib.auth import get_user
from rest_framework import status

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
                common_url, self.guest_client, status.HTTP_201_CREATED
            ],
            [
                self.URL_ANSWER_CREATE.format(
                    telegram_id=self.TELEGRAM_ID,
                    task_number=self.TASK_NUMBER_99
                ), self.guest_client, status.HTTP_404_NOT_FOUND
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
            ).status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            self.guest_client.post(
                common_url,
                data=json.dumps(self.ANSWER_3),
                content_type=self.CONTENT_TYPE_JSON
            ).status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            self.guest_client.post(
                common_url,
                data=json.dumps(self.ANSWER_4),
                content_type=self.CONTENT_TYPE_JSON
            ).status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            self.guest_client.post(
                common_url,
                data=json.dumps(self.ANSWER_5),
                content_type=self.CONTENT_TYPE_JSON
            ).status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_answerbody_answer_create(self):
        """Проверка содержания возвращаемых ответов: answer_create."""
        common_url = self.URL_ANSWER_CREATE.format(
            telegram_id=self.TELEGRAM_ID, task_number=self.TASK_NUMBER_1
        )

        response = self.guest_client.post(
            common_url, data=json.dumps(self.ANSWER_1),
            content_type=self.CONTENT_TYPE_JSON
        )
        self.assertEqual(response.data['number'], int(self.ANSWER_1['number']))
        self.assertEqual(response.data['content'], self.ANSWER_1['content'])
        self.assertEqual(response.get('task'), None)
        answer_id = response.data['id']

        response = self.guest_client.post(
            common_url, data=json.dumps(self.ANSWER_2),
            content_type=self.CONTENT_TYPE_JSON
        )
        self.assertEqual(response.data['number'], int(self.ANSWER_2['number']))
        self.assertEqual(response.data['content'], self.ANSWER_2['content'])
        self.assertEqual(response.data['id'], answer_id)

        response = self.guest_client.post(
            common_url, data=json.dumps(self.ANSWER_3),
            content_type=self.CONTENT_TYPE_JSON
        )
        self.assertEqual(response.data['number'], int(self.ANSWER_3['number']))
        self.assertEqual(response.data['content'], self.ANSWER_3['content'])
        self.assertEqual(response.data['id'], answer_id)

        response = self.guest_client.post(
            common_url, data=json.dumps(self.ANSWER_4),
            content_type=self.CONTENT_TYPE_JSON
        )
        self.assertEqual(response.data['number'], int(self.ANSWER_4['number']))
        self.assertEqual(response.data['content'], self.ANSWER_4['content'])
        self.assertNotEqual(response.data['id'], answer_id)
