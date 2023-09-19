import datetime

from django.urls import reverse
from rest_framework import status

from api.models import Answer, ResultStatus, TaskStatus, UserFromTelegram
from api.tests.test_answer.fixtures import BaseCaseForAnswerTests


class ViewAnswerTests(BaseCaseForAnswerTests):
    """Проверка контроллеров view модуля api."""

    def test_view_answer_create(self):
        """Проверка контроллера answer_create."""
        url = reverse(
            "api:answer_create",
            kwargs={"telegram_id": self.TELEGRAM_ID,
                    "task_number": self.TASK_NUMBER_1},
        )
        user = UserFromTelegram.objects.get(telegram_id=self.TELEGRAM_ID)
        task_status = TaskStatus.objects.get(user=user,
                                             task__number=self.TASK_NUMBER_1)
        ANSWER_1_NUMBER = int(self.ANSWER_1["number"])
        ANSWER_1_CONTENT = self.ANSWER_1["content"]
        self.assertEqual(
            Answer.objects.filter(
                task_status=task_status,
                question__number=ANSWER_1_NUMBER,
                content=ANSWER_1_CONTENT,
            ).exists(),
            False,
        )
        self.client.post(url, data=self.ANSWER_1)
        self.assertEqual(
            Answer.objects.filter(
                task_status=task_status,
                question__number=ANSWER_1_NUMBER,
                content=ANSWER_1_CONTENT,
            ).exists(),
            True,
        )
        self.assertNotEqual(task_status.current_question, ANSWER_1_NUMBER)
        self.assertEqual(
            TaskStatus.objects.get(
                user=user, task__number=self.TASK_NUMBER_1
            ).current_question,
            ANSWER_1_NUMBER,
        )

        self.client.post(url, data=self.ANSWER_2)
        self.assertEqual(
            Answer.objects.filter(
                task_status=task_status,
                question__number=self.ANSWER_2["number"],
                content=self.ANSWER_2["content"],
            ).exists(),
            True,
        )

        self.client.post(url, data=self.ANSWER_4)
        self.assertEqual(
            TaskStatus.objects.get(
                user=user, task__number=self.TASK_NUMBER_1
            ).current_question,
            int(self.ANSWER_4["number"]),
        )

        self.client.post(url, data=self.ANSWER_1)
        self.assertEqual(
            TaskStatus.objects.get(
                user=user, task__number=self.TASK_NUMBER_1
            ).current_question,
            int(self.ANSWER_4["number"]),
        )

    def test_view_task_1_all_answers_exist(self):
        """
        Проверка на запрет расшифровки результата при отсутствии
        всех ответов задания Task_1.
        """
        response = self._setup_task_1_tests(self.LAST_ANSWER_NUMBER - 1)
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            "При отсутствии всех ответов задания Task_1 статус-код"
            " не соответствует ожидаемому."
        )

    def test_view_task_1_status_is_done(self):
        """
        Проверка изменения полей TaskStatus при завершении задания Task_1.
        """
        self._setup_task_1_tests(self.LAST_ANSWER_NUMBER)
        task_status = TaskStatus.objects.get(
            user=self.user_from_telegram, task__number=self.TASK_NUMBER_1
        )
        self.assertTrue(
            task_status.is_done,
            "При завершении задания, поле is_done должно быть \"True\"."
        )
        self.assertTrue(
            isinstance(task_status.pass_date, datetime.datetime),
            "При завершении задания, в поле pass_date не установлено"
            "текущее время."
        )

    def test_view_create_result_status_task_1(self):
        """
        Проверка создания в базе данных расшифрованных результатов ResultStatus
        при получении последнего ответа Задания 1.
        """
        self._setup_task_1_tests(self.LAST_ANSWER_NUMBER)
        task_status = TaskStatus.objects.get(
            user=self.user_from_telegram, task__number=self.TASK_NUMBER_1
        )
        results_status = ResultStatus.objects.filter(
            task_status=task_status).all()
        self.assertTrue(
            results_status.exists(),
            "При завершении Задания 1 в базе данных отсутствуют "
            "расшифрованные результаты"
        )
        result = results_status.first()
        self._assert_has_attributes(result.result, "key", self.RESULT_KEY)
        self._assert_has_attributes(result, "top", self.RESULT_TOP)
        self._assert_has_attributes(result, "score", self.RESULT_SCORE)

    def _setup_task_1_tests(self, last_answer_number):
        url_task_1 = reverse(
            "api:answer_create",
            kwargs={"telegram_id": self.TELEGRAM_ID,
                    "task_number": self.TASK_NUMBER_1},
        )

        task_status = TaskStatus.objects.get(
            user=self.user_from_telegram, task__number=self.TASK_NUMBER_1
        )
        questions = task_status.task.questions.filter(
            number__lt=last_answer_number
        )
        answers = (
            Answer(task_status=task_status, question_id=question.id,
                   content=self.TASK1_ANSWERS_CONTENT[question.number])
            for question in questions
        )
        Answer.objects.bulk_create(answers)
        response = self.client.post(
            url_task_1,
            data={
                "number": self.LAST_ANSWER_NUMBER,
                "content": self.TASK1_ANSWERS_CONTENT[self.LAST_ANSWER_NUMBER]
            }
        )
        return response

    def _assert_has_attributes(self, obj, attr, attr_data):
        """Проверка ожидаемых атрибутов в контексте."""
        error_message = (
            f"В базе данных поле {attr}  расшифрованного результат не "
            "соответствует ожидаемому."
        )
        self.assertEqual(getattr(obj, attr), attr_data, error_message)
