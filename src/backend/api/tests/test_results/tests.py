from rest_framework import status

from api.tests.test_results.fixtures import BaseCaseForResultsTests
from api.views.results import TASK_404, TASK_NOT_COMPLETED, USER_404


class ResultsURLTests(BaseCaseForResultsTests):
    """Тесты api."""

    def test_status_code(self):
        """Проверка доступности и правильности кодов при валидных
         и не валидных запросах."""
        response_correct = self.client.get(self.data['correct'])
        response_incorrect_user = self.client.get(self.data['incorrect_user'])
        response_incorrect_task = self.client.get(self.data['incorrect_task'])
        self.assertEqual(response_correct.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_incorrect_user.status_code, status.HTTP_404_NOT_FOUND
        )
        self.assertEqual(
            response_incorrect_task.status_code, status.HTTP_404_NOT_FOUND
        )

    def test_idempotency(self):
        """Проверка идемпотентности."""
        response_1 = self.client.get(self.data['correct'])
        response_2 = self.client.get(self.data['correct'])
        self.assertEqual(response_1.content, response_2.content)

    def test_template(self):
        """Проверка используемого шаблона."""
        response = self.client.get(self.data['correct'])
        template = 'results/results_for_user_by_task.html'
        self.assertTemplateUsed(response, template)

    def test_context(self):
        """Проверка правильности передаваемого контекста."""
        response = self.client.get(self.data['correct'])
        obj = response.context['result']
        obj_title = obj.title
        obj_description = obj.description
        self.assertEqual(obj_title, self.result.title)
        self.assertEqual(obj_description, self.result.description)

    def test_error_message(self):
        """Проверка правильности сообщений об ошибках."""
        response_incorrect_user = self.client.get(self.data["incorrect_user"])
        response_incorrect_task = self.client.get(self.data["incorrect_task"])
        self.assertEqual(response_incorrect_task.data.get('detail'), TASK_404)
        self.assertEqual(response_incorrect_user.data.get('detail'), USER_404)


class ResultsURLTaskNotCompletedTests(BaseCaseForResultsTests):

    def setUp(self):
        self.task_status.is_done = False
        self.task_status.save()

    def test_task_not_completed(self):
        """Проверка завершенности выполнения конкретного
         задания пользователем."""
        response = self.client.get(self.data['correct'])
        self.assertEqual(response.data.get('detail'), TASK_NOT_COMPLETED)
