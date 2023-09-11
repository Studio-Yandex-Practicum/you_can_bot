from django.urls import reverse

from api.models import TaskStatus, UserFromTelegram
from api.serializers import TaskStatusRetrieveSerializer, TaskStatusSerializer
from api.tests.test_answer.fixtures import BaseCaseForAnswerTests


class ViewTasksTests(BaseCaseForAnswerTests):
    """Проверка контроллеров view модуля tasks."""

    def test_view_tasks(self):
        """Проверка контроллера tasks."""
        common_url = reverse(
            "api:tasks-list",
            kwargs={"telegram_id": self.TELEGRAM_ID},
        )
        first_task_url = reverse(
            "api:tasks-detail",
            kwargs={"telegram_id": self.TELEGRAM_ID,
                    "task__number": self.TASK_NUMBER_1},
        )
        user = UserFromTelegram.objects.get(telegram_id=self.TELEGRAM_ID)
        all_user_tasks = TaskStatus.objects.filter(user=user)
        task_status = TaskStatus.objects.get(
            user=user,
            task__number=self.TASK_NUMBER_1
        )
        expected_responses_data = [
            [common_url, [
                TaskStatusSerializer(task).data for task in all_user_tasks]],
            [first_task_url, TaskStatusRetrieveSerializer(task_status).data]
        ]
        for url, expected_data in expected_responses_data:
            with self.subTest(url=url):
                self.assertEqual(
                    self.client.get(url).data, expected_data
                )
