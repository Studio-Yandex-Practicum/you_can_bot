from http import HTTPStatus

from rest_framework import status

from api.tests.test_question.fixtures import BaseCaseForQuestionTests


class QuestionURLTests(BaseCaseForQuestionTests):
    """Тесты url получения оформленного сообщения."""

    def test_question_url_exists(self):
        """Проверка доступности url."""
        response = self.client.get(self.url["correct"])
        error_message = f"URL: {self.url['correct']} не доступен"
        self.assertEqual(response.status_code, HTTPStatus.OK, error_message)

    def test_question_url_idempotency(self):
        """Проверка запроса на идемпотентность."""
        response_first = self.client.get(self.url["correct"])
        response_second = self.client.get(self.url["correct"])
        error_message = f"Get-запрос: {self.url['correct']} не идемпотентен."
        self.assertEqual(response_first.content, response_second.content, error_message)

    def test_question_url_status_codes(self):
        """Проверка ожидаемых response статусов."""
        status_codes = [
            (
                self.url["correct"],
                status.HTTP_200_OK,
            ),
            (
                self.url["incorrect_task"],
                status.HTTP_404_NOT_FOUND,
            ),
            (
                self.url["incorrect_question"],
                status.HTTP_404_NOT_FOUND,
            ),
        ]
        for url, expected_status in status_codes:
            with self.subTest(url=url):
                error_message = f"Статус код URL {url} не соответствует ожидаемому."
                self.assertEqual(
                    self.client.get(url).status_code, expected_status, error_message
                )

    def test_question_url_uses_correct_template(self):
        """Проверка ожидаемого шаблона."""
        template = "questions/standard_question_format.html"
        response = self.client.get(self.url["correct"])
        error_message = (
            f"Шаблон URL: {self.url['correct']} "
            f"не соответствует ожидаемому: {template}"
        )
        self.assertTemplateUsed(response, template, error_message)
