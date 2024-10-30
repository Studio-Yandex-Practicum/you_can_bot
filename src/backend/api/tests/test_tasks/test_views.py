from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Task, TaskStatus, UserFromTelegram
from api.serializers import TaskStatusRetrieveSerializer, TaskStatusSerializer
from api.tests.test_answer.fixtures import BaseCaseForAnswerTests


class ViewTasksTests(BaseCaseForAnswerTests):
    """Проверка контроллеров view модуля tasks."""

    TASKS_COUNT = 8

    def setUp(self):
        self.common_url = reverse(
            "api:user-tasks-list",
            kwargs={"telegram_id": self.TELEGRAM_ID},
        )
        self.first_task_url = reverse(
            "api:user-tasks-detail",
            kwargs={
                "telegram_id": self.TELEGRAM_ID,
                "task__number": self.TASK_NUMBER_1,
            },
        )
        self.user = UserFromTelegram.objects.get(telegram_id=self.TELEGRAM_ID)
        self.all_user_tasks = TaskStatus.objects.filter(user=self.user)
        self.task_status = TaskStatus.objects.get(
            user=self.user, task__number=self.TASK_NUMBER_1
        )

    def test_view_tasks(self):
        """Проверка контроллера tasks."""

        expected_responses_data = [
            [
                self.common_url,
                TaskStatusSerializer(self.all_user_tasks, many=True).data,
            ],
            [self.first_task_url, TaskStatusRetrieveSerializer(self.task_status).data],
        ]
        for url, expected_data in expected_responses_data:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).data, expected_data)

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
                self.assertEqual(test_data[0].get(field), expected_data)

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
                self.assertEqual(test_data.get(field), expected_data)


class TaskViewSetTests(APITestCase):
    def setUp(self):
        for number in range(1, 4):
            Task.objects.create(number=number, name=f"Задание {number}", end_question=5)

    def test_list_tasks(self):
        response = self.client.get(reverse("api:tasks-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_task(self):
        response = self.client.get(reverse("api:tasks-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number"], 1)
        self.assertEqual(response.data["name"], "Задание 1")

    def test_retrieve_nonexistent_task(self):
        response = self.client.get(reverse("api:tasks-detail", args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_task(self):
        data = {"number": 4, "name": "Задание 4", "end_question": 2}
        response = self.client.post(reverse("api:tasks-list"), data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_task(self):
        data = {"name": "Обновленное Задание 1"}
        response = self.client.patch(reverse("api:tasks-detail", args=[1]), data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_task(self):
        response = self.client.delete(reverse("api:tasks-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(Task.objects.count(), 3)
