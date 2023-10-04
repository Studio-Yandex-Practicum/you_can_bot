from rest_framework import status

from api.tests.test_results.fixtures import BaseCaseForResultsTests
from api.views.results import TASK_404, TASK_NOT_COMPLETED, USER_404


class ResultsURLTests(BaseCaseForResultsTests):
    """Тесты api."""

    def test_status_code(self):
        """Проверка доступности и правильности кодов при валидных
        и не валидных запросах."""

        param_and_status = {
            "correct": status.HTTP_200_OK,
            "incorrect_user": status.HTTP_404_NOT_FOUND,
            "incorrect_task": status.HTTP_404_NOT_FOUND,
        }
        for param, expected_status in param_and_status.items():
            with self.subTest():
                response = self.client.get(self.data[param])
                self.assertEqual(response.status_code, expected_status)

    def test_idempotency(self):
        """Проверка идемпотентности."""
        response_1 = self.client.get(self.data["correct"])
        response_2 = self.client.get(self.data["correct"])
        self.assertEqual(response_1.content, response_2.content)

    def test_template(self):
        """Проверка используемого шаблона."""
        response = self.client.get(self.data["correct"])
        template = "results/standard_result_format.html"
        self.assertTemplateUsed(response, template)

    def test_context(self):
        """Проверка правильности передаваемого контекста."""
        response = self.client.get(self.data["correct"])
        obj = response.context["result"]
        fields = {1: "title", 2: "description"}
        for field in fields.values():
            with self.subTest():
                self.assertEqual(getattr(obj, field), getattr(self.result, field))

    def test_error_message(self):
        """Проверка правильности сообщений об ошибках."""
        param_and_message = {
            "incorrect_user": USER_404,
            "incorrect_task": TASK_404,
        }
        for param, message in param_and_message.items():
            with self.subTest():
                response = self.client.get(self.data[param])
                self.assertEqual(response.data.get("detail"), message)


class ResultsURLTaskNotCompletedTests(BaseCaseForResultsTests):
    def setUp(self):
        self.task_status.is_done = False
        self.task_status.save()

    def test_task_not_completed(self):
        """Проверка завершенности выполнения конкретного
        задания пользователем."""
        response = self.client.get(self.data["correct"])
        self.assertEqual(response.data.get("detail"), TASK_NOT_COMPLETED)
