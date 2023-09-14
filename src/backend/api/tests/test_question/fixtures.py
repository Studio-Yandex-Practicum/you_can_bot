from django.urls import reverse
from rest_framework.test import APITestCase

from api.models import Choice, Question, Task


class BaseCaseForQuestionTests(APITestCase):
    """Базовый набор констант для тестов модуля api."""

    TASK_CORRECT = 1
    END_QUESTION = 10
    TASK_INCORRECT = 99
    QUESTION_NUMBER = 1
    QUESTION_NUMBER_2 = 2
    QUESTION_NUMBER_INCORRECT = 99

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task = Task.objects.create(
            number=cls.TASK_CORRECT, end_question=cls.END_QUESTION
        )
        cls.question = Question.objects.create(
            task=cls.task,
            number=cls.QUESTION_NUMBER,
            content="Просто вопрос",
            example="",
        )
        cls.question_2 = Question.objects.create(
            task=cls.task, number=2, content="вопрос№2", example=""
        )
        choices = (
            Choice(question=cls.question, title="Заголовок1", description="Описание1"),
            Choice(question=cls.question, title="Заголовок2", description="Описание2"),
        )
        Choice.objects.bulk_create(choices)
        cls.url = {
            "correct": reverse(
                "api:get_question",
                kwargs={
                    "question_number": cls.QUESTION_NUMBER,
                    "task_number": cls.TASK_CORRECT,
                },
            ),
            "incorrect_question": reverse(
                "api:get_question",
                kwargs={
                    "question_number": cls.QUESTION_NUMBER_INCORRECT,
                    "task_number": cls.TASK_CORRECT,
                },
            ),
            "incorrect_task": reverse(
                "api:get_question",
                kwargs={
                    "question_number": cls.QUESTION_NUMBER,
                    "task_number": cls.TASK_INCORRECT,
                },
            ),
            "correct_2": reverse(
                "api:get_question",
                kwargs={
                    "question_number": cls.QUESTION_NUMBER_2,
                    "task_number": cls.TASK_CORRECT,
                },
            ),
        }
