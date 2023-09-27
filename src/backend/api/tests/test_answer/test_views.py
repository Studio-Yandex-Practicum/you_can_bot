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
            kwargs={"telegram_id": self.TELEGRAM_ID, "task_number": self.TASK_NUMBER_1},
        )
        user = UserFromTelegram.objects.get(telegram_id=self.TELEGRAM_ID)
        task_status = TaskStatus.objects.get(user=user, task__number=self.TASK_NUMBER_1)
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

    def test_view_tasks_all_answers_exist(self):
        """
        Проверка на запрет расшифровки результата при отсутствии
        всех ответов в Заданиях.
        """
        setup_functions = {
            1: self._setup_task_1_tests,
            2: self._setup_task_2_tests,
            3: self._setup_task_3_tests,
        }
        for task_number in range(1, self.TASK_COUNT + 1):
            with self.subTest(task_number=task_number):
                response = setup_functions[task_number](is_all_answers=False)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_404_NOT_FOUND,
                    f"При отсутствии всех ответов Задания №{task_number}"
                    " статус-код не соответствует ожидаемому.",
                )

    def test_view_tasks_status_is_done(self):
        """
        Проверка изменения полей TaskStatus при завершении Заданий.
        """
        setup_functions = {
            1: self._setup_task_1_tests,
            2: self._setup_task_2_tests,
            3: self._setup_task_3_tests,
        }
        for task_number in range(1, self.TASK_COUNT + 1):
            with self.subTest(task_number=task_number):
                setup_functions[task_number]()
                task_status = TaskStatus.objects.get(
                    user=self.user_from_telegram, task__number=task_number
                )
                self.assertTrue(
                    task_status.is_done,
                    f'При завершении Задания №{task_number}, поле "is_done"'
                    " должно быть True.",
                )
                self.assertTrue(
                    isinstance(task_status.pass_date, datetime.datetime),
                    f'При завершении Задания №{task_number}, в поле "pass_date"'
                    " не установлено текущее время.",
                )

    def test_view_create_result_status_task_1(self):
        """
        Проверка создания в базе данных расшифрованных результатов ResultStatus
        при получении последнего ответа Задания №1.
        """
        self._setup_task_1_tests()
        results_status = ResultStatus.objects.filter(
            task_status=self.tasks_status[self.TASK_NUMBER_1]
        ).all()
        self.assertTrue(
            results_status.exists(),
            "При завершении Задания №1 в базе данных отсутствуют "
            "расшифрованные результаты",
        )
        result = results_status.first()
        self._assert_has_attributes(
            self.TASK_NUMBER_1, result.result, "key", self.RESULT_KEY_TASK_1
        )
        self._assert_has_attributes(
            self.TASK_NUMBER_1, result, "top", self.RESULT_TOP_TASK_1
        )
        self._assert_has_attributes(
            self.TASK_NUMBER_1, result, "score", self.RESULT_SCORE_TASK_1
        )

    def test_view_create_result_status_task_2(self):
        """
        Проверка создания в базе данных расшифрованных результатов ResultStatus
        при получении последнего ответа Задания №2.
        """
        self._setup_task_2_tests(is_all_answers=True)
        results_status = ResultStatus.objects.filter(
            task_status=self.tasks_status[self.TASK_NUMBER_2]
        ).all()
        self.assertTrue(
            results_status.exists(),
            "При завершении Задания №2 в базе данных отсутствуют "
            "расшифрованные результаты",
        )
        result = results_status.first()
        self._assert_has_attributes(
            self.TASK_NUMBER_2, result.result, "key", self.RESULT_KEY_TASK_2
        )
        self._assert_has_attributes(
            self.TASK_NUMBER_2, result, "top", self.RESULT_TOP_TASK_2
        )

    def test_view_create_result_status_task_3(self):
        """
        Проверка создания в базе данных расшифрованных результатов ResultStatus
        при получении последнего ответа Задания №3.
        """
        self._setup_task_3_tests()
        results_status = ResultStatus.objects.filter(
            task_status=self.tasks_status[self.TASK_NUMBER_3]
        ).all()
        self.assertTrue(
            results_status.exists(),
            "При завершении Задания №3 в базе данных отсутствуют "
            "расшифрованные результаты",
        )
        result = results_status.first()
        self._assert_has_attributes(
            self.TASK_NUMBER_3, result.result, "key", self.RESULT_KEY_TASK_3
        )
        self._assert_has_attributes(
            self.TASK_NUMBER_3, result, "top", self.RESULT_TOP_TASK_3
        )
        self._assert_has_attributes(
            self.TASK_NUMBER_3, result, "score", self.RESULT_SCORE_TASK_3
        )

    def _setup_task_1_tests(self, is_all_answers: bool = True):
        task_status = self.tasks_status[self.TASK_NUMBER_1]
        url_task = reverse(
            "api:answer_create",
            kwargs={"telegram_id": self.TELEGRAM_ID, "task_number": self.TASK_NUMBER_1},
        )
        questions = self._get_task_questions(self.TASK_NUMBER_1, is_all_answers)
        answers = (
            Answer(
                task_status=task_status,
                question_id=question.id,
                content=self.TASK1_ANSWERS_CONTENT[question.number],
            )
            for question in questions
        )
        Answer.objects.bulk_create(answers)
        response = self.client.post(
            url_task,
            data={
                "number": task_status.task.end_question,
                "content": self.TASK1_ANSWERS_CONTENT[task_status.task.end_question],
            },
        )
        return response

    def _setup_task_2_tests(self, is_all_answers: bool = True):
        task_status = self.tasks_status[self.TASK_NUMBER_2]
        url_task = reverse(
            "api:answer_create",
            kwargs={"telegram_id": self.TELEGRAM_ID, "task_number": self.TASK_NUMBER_2},
        )
        questions = self._get_task_questions(self.TASK_NUMBER_2, is_all_answers)
        answers = (
            Answer(
                task_status=task_status,
                question_id=question.id,
                content="б",
            )
            for question in questions
        )
        Answer.objects.bulk_create(answers)
        response = self.client.post(
            url_task,
            data={
                "number": task_status.task.end_question,
                "content": "а",
            },
        )
        return response

    def _setup_task_3_tests(self, is_all_answers: bool = True):
        task_status = self.tasks_status[self.TASK_NUMBER_3]
        url_task = reverse(
            "api:answer_create",
            kwargs={"telegram_id": self.TELEGRAM_ID, "task_number": self.TASK_NUMBER_3},
        )
        questions = self._get_task_questions(self.TASK_NUMBER_3, is_all_answers)
        answers = (
            Answer(
                task_status=task_status,
                question_id=question.id,
                content="б",
            )
            for question in questions
        )
        Answer.objects.bulk_create(answers)
        response = self.client.post(
            url_task,
            data={
                "number": task_status.task.end_question,
                "content": "б",
            },
        )
        return response

    def _get_task_questions(self, task_number, is_all_answers):
        """
        Получение списка объектов вопросов Задания.
        Args:
            is_all_answers (bool): False при тестировании не полного
                                   количества ответов.
        """
        last_number = self.tasks_status[task_number].task.end_question
        if not is_all_answers:
            last_number -= 1
        return self.tasks_status[task_number].task.questions.filter(
            number__lt=last_number
        )

    def _assert_has_attributes(self, task_number, obj, attr, attr_data):
        """Проверка ожидаемых атрибутов в контексте."""
        error_message = (
            f'В базе данных Задания №{task_number} поле "{attr}" '
            "расшифрованного результата не соответствует ожидаемому."
        )
        self.assertEqual(getattr(obj, attr), attr_data, error_message)
