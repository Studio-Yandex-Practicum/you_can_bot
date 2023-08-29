from django.test import TestCase

from api.calculation_service import task_4
from api.models import Answer

QUESTIONS_NUMBER = 42


class TestTask4(TestCase):
    def test_transform_answers_to_dict(self):
        """
        Тестирует преобразование списка объектов Answers в словарь.
        """
        test_content = '5'
        test_user_answers = [
            Answer(number=i, content=test_content)
            for i in range(1, QUESTIONS_NUMBER + 1)
        ]
        expected = {
            number: int(test_content)
            for number in range(1, QUESTIONS_NUMBER + 1)
        }
        recieved = task_4._transform_answers_to_dict(test_user_answers)
        self.assertEquals(recieved, expected)

    def test_calculate_scales_avg_score(self):
        """
        Тестирует расчет среднего балла по каждой шкале.
        """
        test_scales_scores = {
            1: 6, 2: 4, 3: 9, 4: 1, 5: 10, 6: 6, 7: 9, 8: 7, 9: 10, 10: 8,
            11: 4, 12: 2, 13: 6, 14: 4, 15: 5, 16: 6, 17: 7, 18: 8, 19: 9,
            20: 5, 21: 4, 22: 1, 23: 10, 24: 7, 25: 5, 26: 7, 27: 3, 28: 4,
            29: 2, 30: 6, 31: 1, 32: 9, 33: 6, 34: 8, 35: 10, 36: 3, 37: 5,
            38: 6, 39: 3, 40: 9, 41: 6
        }

        expected = {
            '1': 6.8, '2': 7, '3': 7, '4': 2, '5': 5,
            '6': 5.4, '7': 4.6, '8': 5.6, '9': 7.6
        }
        recieved = task_4._calculate_scales_avg_score(test_scales_scores)
        self.assertEquals(recieved, expected)

    def test_get_top_features_sorted(self):
        """
        Тестирует, что функция возвращает отсортированный
        по невозрастанию список шкал, чей средний балл выше 6.
        """
        test_scales_scores = {
            'several_scales_meet_requirements': {
                '1': 6, '2': 1, '3': 10, '4': 6.1, '5': 5,
                '6': 6.4, '7': 4.6, '8': 6.1, '9': 7.6
            },
            'one_scale_meets_requirements': {
                '1': 4, '2': 1, '3': 3.6, '4': 6.1, '5': 3,
                '6': 2, '7': 4.6, '8': 5.5, '9': 6
            },
            'none_of_scales_meet_requirements': {
                '1': 1.2, '2': 1, '3': 5, '4': 3, '5': 4,
                '6': 3, '7': 4.6, '8': 6, '9': 2
            }
        }
        expected = [
            ['3', '9', '6', '4', '8'],
            ['4'],
            []
        ]
        for test_name, expected in zip(test_scales_scores, expected):
            with self.subTest(test_name=test_name):
                recieved = task_4._get_top_features_sorted(
                    test_scales_scores[test_name])
                self.assertEquals(recieved, expected)

    def test_write_result_to_string(self):
        """Проверяет корректность формирования результирующей строки."""
        test_scales_options = [['3', '9', '1'], ['1'], []]
        expected = ['3 9 1', '1', '0']
        for test_scale, expected in zip(test_scales_options, expected):
            with self.subTest(test_scale=test_scale):
                recieved = task_4._write_result_to_string(test_scale)
                self.assertEquals(recieved, expected)
