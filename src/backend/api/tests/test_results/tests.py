from api.tests.test_results.fixtures import BaseCaseForResultsTests
from rest_framework import status


# Доступность +
# Идемпотентность +
# Верный код ответа при валидном запросе +
# Использование ожидаемого HTML-шаблона +
# В шаблон передан правильный контекст +
# Верный код ответа при отсутствии задания или пользователя +
# Верное сообщение об ошибке для задания/пользователя
# Верный код ответа для невалидного запроса, когда задание ещё не пройдено, а также сообщение об ошибке

class ResultsURLTests(BaseCaseForResultsTests):
    """Тест url."""

    def test_status_code_get_results(self):
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
            response_incorrect_task.status_code, status.HTTP_404_NOT_FOUND)

    def test_idempotency_get_results(self):
        """Проверка идемпотентности."""
        response_1 = self.client.get(self.data['correct'])
        response_2 = self.client.get(self.data['correct'])
        self.assertEqual(response_1.content, response_2.content)

    def test_correct_template(self):
        """Проверка используемого шаблона."""
        response = self.client.get(self.data['correct'])
        template = 'results/results_for_user_by_task.html'
        self.assertTemplateUsed(response, template)

    def test_correct_context(self):
        """Проверка правильности передаваемого контекста."""
        response = self.client.get(self.data['correct'])
        obj = response.context['result']
        obj_title = obj.title
        obj_description = obj.description

        self.assertEqual(obj_title, self.result.title)
        self.assertEqual(obj_description, self.result.description)