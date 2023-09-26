import logging

from django.test import TestCase
from rest_framework.serializers import ValidationError

from api.calculation_service.task_1 import _get_result_points
from api.models import Answer


class TestTask1(TestCase):
    """Тестирует корректность алгоритма вычисления
    результата по первому тесту."""

    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)

    def test_task_1_same_answers(self):
        """Правильно определилась расшифровка с одинаковым ответом на все
        вопросы по первому заданию."""
        answers = [Answer(content="012345") for _ in range(10)]
        self.assertEqual(
            [(50, "Е"), (40, "Д"), (30, "Г")], _get_result_points(answers)[:3]
        )

    def test_task_1_different_answers(self):
        """Правильно определилась расшифровка с различными ответами
        по первому заданию."""
        answers_content = (
            "543210",
            "053142",
            "123504",
            "041235",
            "012345",
            "410523",
            "321054",
            "013245",
            "543012",
            "230451",
        )
        answers = [Answer(content=answer) for answer in answers_content]
        self.assertEqual(
            [(31, "Е"), (29, "Д"), (27, "Б")], _get_result_points(answers)[:3]
        )

    def test_task_1_inconsistent_answer_content(self):
        """Неконсистентный Answer.content прервал выполнение проверки."""
        with self.assertRaises(ValidationError):
            _get_result_points([Answer(content="12345")])

        with self.assertRaises(ValidationError):
            _get_result_points([Answer(content=None)])

        # Консистентный Answer.content был посчитан корректно
        self.assertEqual(
            [(5, "Е"), (4, "Д"), (3, "Г")],
            _get_result_points([Answer(content="012345")])[:3],
        )

    def test_task_1_more_than_one_third_place(self):
        """Правильно определилась расшифровка с одинаковым количеством баллов
        у третьего, четвертого и остальных мест по первому заданию."""
        self.assertEqual(
            [(5, "Е"), (5, "Д"), (5, "Г"), (5, "В"), (5, "Б"), (5, "А")],
            _get_result_points([Answer(content="555555")]),
        )
        self.assertEqual(
            [(5, "Е"), (5, "Д"), (5, "Г"), (5, "В"), (1, "Б"), (1, "А")],
            _get_result_points([Answer(content="115555")]),
        )

        # Контент соответствующий реальным ответам на тесты,
        # но третье место делят сразу два качества.
        real_ten_answers_content = (
            "243510",
            "053142",
            "123504",
            "041235",
            "012345",
            "410523",
            "321054",
            "013245",
            "543012",
            "230451",
        )
        answers = [Answer(content=answer) for answer in real_ten_answers_content]

        self.assertEqual(
            [(31, "Е"), (29, "Д"), (27, "Г"), (27, "Б")],
            _get_result_points(answers)[:4],
        )

    def tearDown(self) -> None:
        logging.disable(logging.NOTSET)
