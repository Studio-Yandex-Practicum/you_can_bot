from django.urls import reverse

from api.models import TaskStatus, UserFromTelegram
from api.serializers import TaskStatusRetrieveSerializer, TaskStatusSerializer
from api.tests.test_answer.fixtures import BaseCaseForAnswerTests


class ViewTasksTests(BaseCaseForAnswerTests):
    """Проверка контроллеров view модуля tasks."""

    TASKS_COUNT = 8

    def setUp(self):
        self.common_url = reverse(
            "api:tasks-list",
            kwargs={"telegram_id": self.TELEGRAM_ID},
        )
        self.first_task_url = reverse(
            "api:tasks-detail",
            kwargs={"telegram_id": self.TELEGRAM_ID,
                    "task__number": self.TASK_NUMBER_1},
        )
        self.user = UserFromTelegram.objects.get(telegram_id=self.TELEGRAM_ID)
        self.all_user_tasks = TaskStatus.objects.filter(user=self.user)
        self.task_status = TaskStatus.objects.get(
            user=self.user,
            task__number=self.TASK_NUMBER_1
        )

    def test_view_tasks(self):
        """Проверка контроллера tasks."""

        expected_responses_data = [
            [self.common_url,
                TaskStatusSerializer(self.all_user_tasks, many=True).data],
            [self.first_task_url,
                TaskStatusRetrieveSerializer(self.task_status).data]
        ]
        for url, expected_data in expected_responses_data:
            with self.subTest(url=url):
                self.assertEqual(
                    self.client.get(url).data, expected_data
                )

    def test_TaskStatusSerializer(self):
        """Проверка сериализатора для tasks-list."""
        response = self.client.get(self.common_url)
        test_data = response.json()

        expected_responses_data = [
            ["number", self.TASK_NUMBER_1],
            ["is_done", self.task_status.is_done],
        ]
        self.assertEqual(len(test_data), self.TASKS_COUNT)
        for field, expected_data in expected_responses_data:
            with self.subTest(field=field):
                self.assertEqual(
                    test_data[0].get(field), expected_data
                )

    def test_TaskStatusRetrieveSerializer(self):
        """Проверка сериализатора для tasks-detail."""
        response = self.client.get(self.first_task_url)
        test_data = response.json()
        expected_responses_data = [
            ["number", self.TASK_NUMBER_1],
            ["current_question", self.task_status.current_question],
            ["is_done", self.task_status.is_done],
        ]
        for field, expected_data in expected_responses_data:
            with self.subTest(field=field):
                self.assertEqual(
                    test_data.get(field), expected_data
                )
