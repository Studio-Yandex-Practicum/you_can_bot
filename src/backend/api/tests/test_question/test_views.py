from django.conf import settings

from api.tests.test_question.fixtures import BaseCaseForQuestionTests


class QuestionViewTests(BaseCaseForQuestionTests):
    """Тесты view получения оформленного сообщения."""
    QUESTION_ERROR_MESSAGE = "Не найден вопрос с таким номером."
    TASK_ERROR_MESSAGE = "Не найдено задание с таким номером."
    CONTENT = "<b>2. вопрос№2</b>\n\n\n"

    def test_question_get_correct_json_data(self):
        """Проверка response на формирование правильного json данных."""
        error_message = (
            "Json ответ не соответствует ожидаемому."
        )
        response = self.client.get(self.url["correct_2"])
        response_content = str(response.content, encoding='utf8')
        self.assertJSONEqual(
            response_content,
            {
                "count": 1,
                "result": [
                    {
                        "content": self.CONTENT
                    }
                ],
            },
            error_message
        )

    def test_question_get_correct_context(self):
        """Проверка response на формирование правильного контекста."""
        question = self.question

        response = self.client.get(self.url["correct"])
        context_question = response.context.get("question")
        error_message = "В контекст шаблона не передан question"
        self.assertIsNotNone(context_question, error_message)

        self._assert_has_attributes(context_question, question, "number")
        self._assert_has_attributes(context_question, question, "content")
        self._assert_has_attributes(context_question, question, "choices")

        context_choice = response.context["question"].choices.first()
        choice = question.choices.first()
        self._assert_has_attributes(context_choice, choice, "title")
        self._assert_has_attributes(context_choice, choice, "description")

    def test_question_expected_not_found_message(self):
        """Проверка ожидаемых сообщений об ошибке."""
        messages = [
            (self.url["incorrect_task"],
             settings.NOT_FOUND_TASK_ERROR_MESSAGE,),
            (self.url["incorrect_question"],
             settings.NOT_FOUND_QUESTION_ERROR_MESSAGE,),
        ]
        for num, (url, expected_message) in enumerate(messages):
            error_message = (
                "Сообщение об ошибке при отсутствии вопроса/задания "
                "не соответствует ожидаемому."
            )
            response = self.client.get(url)
            self.assertEqual(
                str(response.data.get("detail")),
                self.QUESTION_ERROR_MESSAGE if num else
                self.TASK_ERROR_MESSAGE,
                error_message
            )

    def _assert_has_attributes(self, context, obj, attr):
        """Проверка ожидаемых атрибутов в контексте."""
        error_message = (
            f"В контекст {context._meta.model_name} не передан атрибут {attr}"
        )
        self.assertEqual(getattr(context, attr), getattr(obj, attr),
                         error_message)
