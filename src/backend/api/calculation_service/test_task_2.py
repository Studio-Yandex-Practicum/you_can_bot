from django.test import TestCase
from rest_framework.serializers import ValidationError

from api.models import Answer
from .task_1 import calculate_task_1_result


class TestTask1(TestCase):
    """Тестирует корректность алгоритма вычисления
    результата по первому тесту."""

    def test_task_1_same_answers(self):
        """Правильно определилась расшифровка с одинаковым ответом на все
        вопросы по первому заданию."""
        answers = [Answer(content='012345') for _ in range(10)]
        self.assertEqual('Е;50\nД;40\nГ;30', calculate_task_1_result(answers))

    def test_task_1_different_answers(self):
        """Правильно определилась расшифровка с различными ответами
        по первому заданию."""
        answers_content = (
            '543210', '053142', '123504', '041235', '012345', '410523',
            '321054', '013245', '543012', '230451'
        )
        answers = [Answer(content=answer) for answer in answers_content]
        self.assertEqual('Е;31\nД;29\nБ;27', calculate_task_1_result(answers))

    def test_task_1_inconsistent_answer_content(self):
        """Неконсистентный Answer.content прервал выполнение проверки."""
        with self.assertRaises(ValidationError):
            calculate_task_1_result([Answer(content='12345')])

        with self.assertRaises(ValidationError):
            calculate_task_1_result([Answer(content=None)])

        # Консистентный Answer.content был посчитан корректно
        self.assertEqual(
            'Е;5\nД;4\nГ;3',
            calculate_task_1_result([Answer(content='012345')])
        )

    def test_task_1_more_than_one_third_place(self):
        """Правильно определилась расшифровка с одинаковым количеством баллов
        у третьего, четвертого и остальных мест по первому заданию."""
        self.assertEqual(
            'Е;5\nД;5\nГ;5\nВ;5\nБ;5\nА;5',
            calculate_task_1_result([Answer(content='555555')])
        )
        self.assertEqual(
            'Е;5\nД;5\nГ;5\nВ;5',
            calculate_task_1_result([Answer(content='115555')])
        )

        # Контент соответствующий реальным ответам на тесты,
        # но третье место делят сразу два качества.
        real_ten_answers_content = (
            '243510', '053142', '123504', '041235', '012345', '410523',
            '321054', '013245', '543012', '230451'
        )
        answers = [
            Answer(content=answer) for answer in real_ten_answers_content
        ]

        self.assertEqual(
            'Е;31\nД;29\nГ;27\nБ;27',
            calculate_task_1_result(answers)
        )
