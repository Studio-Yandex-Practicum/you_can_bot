from django.test import TestCase

from api.calculation_service import task_4
from api.models import Answer, Question, Task, TaskStatus, UserFromTelegram

QUESTIONS_NUMBER = 42


class TestTask4(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        test_string = "test_string"
        cls.user = UserFromTelegram.objects.create(
            telegram_id=88294221,
            telegram_username=test_string,
            name=test_string,
            surname=test_string,
        )
        cls.task_status = TaskStatus.objects.get(
            user=cls.user,
            task__number=4,
        )
        questions = [
            Question(task=Task.objects.get(number=4), number=question_number)
            for question_number in range(1, QUESTIONS_NUMBER + 1)
        ]
        Question.objects.bulk_create(questions)
        cls.questions = Question.objects.filter(task=4)

    def test_transform_answers_to_dict(self):
        """
        Тестирует преобразование списка объектов Answers в словарь.
        """
        test_content = "5"
        test_user_answers = [
            Answer(question=question, content=test_content)
            for question in self.questions
        ]
        expected = {
            number: int(test_content) for number in range(1, QUESTIONS_NUMBER + 1)
        }
        received = task_4._transform_answers_to_dict(test_user_answers)
        self.assertEquals(received, expected)

    def test_calculate_scales_avg_score(self):
        """
        Тестирует расчет среднего балла по каждой шкале.
        """
        # fmt: off
        test_scales_scores = {
            1: 6, 2: 4, 3: 9, 4: 1, 5: 10, 6: 6, 7: 9, 8: 7, 9: 10, 10: 8,
            11: 4, 12: 2, 13: 6, 14: 4, 15: 5, 16: 6, 17: 7, 18: 8, 19: 9,
            20: 5, 21: 4, 22: 1, 23: 10, 24: 7, 25: 5, 26: 7, 27: 3, 28: 4,
            29: 2, 30: 6, 31: 1, 32: 9, 33: 6, 34: 8, 35: 10, 36: 3, 37: 5,
            38: 6, 39: 3, 40: 9, 41: 6
        }

        expected = {
            "1": 6.8, "2": 7, "3": 7, "4": 2, "5": 5,
            "6": 5.4, "7": 4.6, "8": 5.6, "9": 7.6
        }
        # fmt: on
        received = task_4._calculate_scales_avg_score(test_scales_scores)
        self.assertEquals(received, expected)

    def test_get_top_features_sorted(self):
        """
        Тестирует, что функция возвращает отсортированный
        по невозрастанию список шкал, чей средний балл выше 6.
        """
        # fmt: off
        test_scales_scores = {
            "several_scales_meet_requirements": {
                "1": 6, "2": 1, "3": 10, "4": 6.1, "5": 5,
                "6": 6.4, "7": 4.6, "8": 6.1, "9": 7.6
            },
            "one_scale_meets_requirements": {
                "1": 4, "2": 1, "3": 3.6, "4": 6, "5": 3,
                "6": 2, "7": 4.6, "8": 5.5, "9": 5.9
            },
            "none_of_scales_meet_requirements": {
                "1": 1.2, "2": 1, "3": 5, "4": 3, "5": 4,
                "6": 3, "7": 4.6, "8": 5, "9": 2
            }
        }
        # fmt: on
        expected = [
            [("3", 10), ("9", 7.6), ("6", 6.4), ("4", 6.1), ("8", 6.1), ("1", 6)],
            [("4", 6)],
            [("3", 5), ("8", 5)],
        ]
        for test_name, expected in zip(test_scales_scores, expected):
            with self.subTest(test_name=test_name):
                received = task_4._get_top_features_sorted(
                    test_scales_scores[test_name]
                )
                self.assertEquals(received, expected)
