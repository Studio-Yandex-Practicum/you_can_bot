from django.urls import reverse

from api.models import Answer, TaskStatus, UserFromTelegram
from api.tests.test_case import BaseCaseForTests


class ViewTests(BaseCaseForTests):
    """Проверка контроллеров view модуля api."""

    def test_view_answer_create(self):
        """Проверка контроллера answer_create."""
        url = reverse(
            "answer_create",
            kwargs={"telegram_id": self.TELEGRAM_ID, "task_number": self.TASK_NUMBER_1},
        )
        user = UserFromTelegram.objects.get(telegram_id=self.TELEGRAM_ID)
        task = TaskStatus.objects.get(user=user, number=self.TASK_NUMBER_1)
        ANSWER_1_NUMBER = int(self.ANSWER_1["number"])
        ANSWER_1_CONTENT = self.ANSWER_1["content"]
        self.assertEqual(
            Answer.objects.filter(
                task=task, number=ANSWER_1_NUMBER, content=ANSWER_1_CONTENT
            ).exists(),
            False,
        )
        self.client.post(url, data=self.ANSWER_1)
        self.assertEqual(
            Answer.objects.filter(
                task=task, number=ANSWER_1_NUMBER, content=ANSWER_1_CONTENT
            ).exists(),
            True,
        )
        self.assertNotEqual(task.current_question, ANSWER_1_NUMBER)
        self.assertEqual(
            TaskStatus.objects.get(
                user=user, number=self.TASK_NUMBER_1
            ).current_question,
            ANSWER_1_NUMBER,
        )

        self.client.post(url, data=self.ANSWER_2)
        self.assertEqual(
            Answer.objects.filter(
                task=task,
                number=self.ANSWER_2["number"],
                content=self.ANSWER_2["content"],
            ).exists(),
            True,
        )

        self.client.post(url, data=self.ANSWER_4)
        self.assertEqual(
            TaskStatus.objects.get(
                user=user, number=self.TASK_NUMBER_1
            ).current_question,
            int(self.ANSWER_4["number"]),
        )

        self.client.post(url, data=self.ANSWER_1)
        self.assertEqual(
            TaskStatus.objects.get(
                user=user, number=self.TASK_NUMBER_1
            ).current_question,
            int(self.ANSWER_4["number"]),
        )
