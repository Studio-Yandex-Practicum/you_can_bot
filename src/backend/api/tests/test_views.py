import json

from django.contrib.auth import get_user

from api.models import Answer, TaskStatus, UserFromTelegram
from api.tests.test_case import BaseCaseForTests


class ViewTests(BaseCaseForTests):
    """Проверка контроллеров view модуля api."""

    def test_view_answer_create(self):
        """Проверка контроллера answer_create."""
        url = self.URL_ANSWER_CREATE.format(
            telegram_id=self.TELEGRAM_ID, task_number=self.TASK_NUMBER_1
        )
        user = UserFromTelegram.objects.get(telegram_id=self.TELEGRAM_ID)
        task = TaskStatus.objects.get(user=user, number=self.TASK_NUMBER_1)
        ANSWER_1_NUMBER = int(self.ANSWER_1['number'])
        ANSWER_1_CONTENT = self.ANSWER_1['content']
        self.assertEqual(
            Answer.objects.filter(
                task=task, number=ANSWER_1_NUMBER,
                content=ANSWER_1_CONTENT
            ).exists(),
            False
        )
        self.guest_client.post(
            url,
            data=json.dumps(self.ANSWER_1),
            content_type=self.CONTENT_TYPE_JSON
        )
        self.assertEqual(
            Answer.objects.filter(
                task=task, number=ANSWER_1_NUMBER, content=ANSWER_1_CONTENT
            ).exists(),
            True
        )
        self.assertNotEqual(task.current_question, ANSWER_1_NUMBER)
        self.assertEqual(
            TaskStatus.objects.get(
                user=user, number=self.TASK_NUMBER_1).current_question,
                ANSWER_1_NUMBER
        )

        self.guest_client.post(
            url,
            data=json.dumps(self.ANSWER_2),
            content_type=self.CONTENT_TYPE_JSON
        )
        self.assertEqual(
            Answer.objects.filter(
                task=task,
                number=self.ANSWER_2['number'],
                content=self.ANSWER_2['content']
            ).exists(),
            True
        )

        self.guest_client.post(
            url,
            data=json.dumps(self.ANSWER_4),
            content_type=self.CONTENT_TYPE_JSON
        )
        self.assertEqual(
            TaskStatus.objects.get(
                user=user, number=self.TASK_NUMBER_1).current_question,
                int(self.ANSWER_4['number'])
        )

        self.guest_client.post(
            url,
            data=json.dumps(self.ANSWER_1),
            content_type=self.CONTENT_TYPE_JSON
        )
        self.assertEqual(
            TaskStatus.objects.get(
                user=user, number=self.TASK_NUMBER_1).current_question,
                int(self.ANSWER_4['number'])
        )
