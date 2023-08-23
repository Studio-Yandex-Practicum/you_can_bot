from django.test import TestCase

from api.models import Answer
from .task_1 import calculate_task_1_result


class TestTask1(TestCase):
    """Тестирует корректность алгоритма вычисления
    результата по первому тесту."""

    def test_task_1_same_answers(self):
        """Правильно определилась расшифровка с одинаковым ответом на все
        вопросы по первому заданию."""
        answers = [Answer(content='012345') for _ in range(10)]
        self.assertEqual('ЕДГ', calculate_task_1_result(answers))

    def test_task_1_different_answers(self):
        """Правильно определилась расшифровка с различными ответами
        по первому заданию."""
        answers_content = (
            '543210', '053142', '123504', '041235', '012345', '410523',
            '321054', '013245', '543012', '230451'
        )
        answers = [Answer(content=answer) for answer in answers_content]
        self.assertEqual('ЕДБ', calculate_task_1_result(answers))
