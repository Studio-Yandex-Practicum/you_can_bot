from django.test import TestCase

from api.calculation_service import task_3
from api.models import Answer, Question, Task, TaskStatus, UserFromTelegram


class TestTask3(TestCase):
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
            task__number=3,
        )
        # fmt: off
        test_user_answers = {
            1: 'а', 2: 'а', 3: 'б', 4: 'а', 5: 'б', 6: 'а', 7: 'б',
            8: 'а', 9: 'а', 10: 'б', 11: 'а', 12: 'б', 13: 'а', 14: 'б',
            15: 'а', 16: 'а', 17: 'б', 18: 'а', 19: 'б', 20: 'а', 21: 'б',
            22: 'а', 23: 'а', 24: 'б', 25: 'а', 26: 'б', 27: 'а', 28: 'б',
            29: 'а', 30: 'а', 31: 'б', 32: 'а', 33: 'б', 34: 'а', 35: 'б',
            36: 'а', 37: 'а', 38: 'б', 39: 'а', 40: 'б', 41: 'а', 42: 'б',
        }
        # fmt: on
        questions = [
            Question(task=Task.objects.get(number=2), number=question_number)
            for question_number in test_user_answers.keys()
        ]
        Question.objects.bulk_create(questions)
        answers = [
            Answer(task_status=cls.task_status, question=question, content=choice)
            for question, choice in zip(questions, test_user_answers.values())
        ]
        Answer.objects.bulk_create(answers)
        cls.user_answers = Answer.objects.filter(task_status=cls.task_status)

    def test_distribute_answers_by_scales(self):
        """
        Тестирует распределение ответов пользователя
        по шкалам и подсчет кол-ва баллов.
        """

        expected = {
            "scale_1": 6,
            "scale_4": 9,
            "scale_6": 7,
            "scale_2": 9,
            "scale_3": 5,
            "scale_5": 6,
        }
        received = task_3._distribute_answers_by_scales(self.user_answers.all())
        self.assertEquals(received, expected)

    def test_sorted_scales_in_non_growing_order(self):
        """
        Тестирует корректность сортировки словаря с кол-вом ответов по шкалам.
        """
        test_scale_scores_counters = {
            "all_scores_different": {
                "scale_2": 8,
                "scale_5": 9,
                "scale_4": 10,
                "scale_6": 4,
                "scale_1": 6,
                "scale_3": 5,
            },
            "some_scores_equals": {
                "scale_4": 8,
                "scale_1": 10,
                "scale_3": 3,
                "scale_2": 8,
                "scale_6": 9,
                "scale_5": 4,
            },
            "all_scores_equals": {
                "scale_5": 7,
                "scale_2": 7,
                "scale_1": 7,
                "scale_3": 7,
                "scale_4": 7,
                "scale_6": 7,
            },
        }
        expected = [
            [
                ("scale_4", 10),
                ("scale_5", 9),
                ("scale_2", 8),
                ("scale_1", 6),
                ("scale_3", 5),
                ("scale_6", 4),
            ],
            [
                ("scale_1", 10),
                ("scale_6", 9),
                ("scale_2", 8),
                ("scale_4", 8),
                ("scale_5", 4),
                ("scale_3", 3),
            ],
            [
                ("scale_1", 7),
                ("scale_2", 7),
                ("scale_3", 7),
                ("scale_4", 7),
                ("scale_5", 7),
                ("scale_6", 7),
            ],
        ]
        for test_name, expected in zip(test_scale_scores_counters, expected):
            with self.subTest(test_name=test_name):
                received = task_3._sorted_scales_in_non_growing_order(
                    test_scale_scores_counters[test_name]
                )
                self.assertEquals(received, expected)

    def test_make_top_scales_by_scores(self):
        """
        Тестирует выбор шкал с наибольшим кол-вом баллов (топ 3).
        """
        test_scale_scores_counters = {
            "3_leaders": [
                ("scale_3", 10),
                ("scale_1", 9),
                ("scale_5", 8),
                ("scale_4", 6),
                ("scale_2", 5),
                ("scale_6", 4),
            ],
            "4 leaders": [
                ("scale_1", 10),
                ("scale_3", 9),
                ("scale_2", 8),
                ("scale_6", 8),
                ("scale_4", 4),
                ("scale_5", 3),
            ],
            "all_scores_equals": [
                ("scale_1", 7),
                ("scale_2", 7),
                ("scale_3", 7),
                ("scale_4", 7),
                ("scale_5", 7),
                ("scale_6", 7),
            ],
        }
        expected = [
            [("scale_3", 10), ("scale_1", 9), ("scale_5", 8)],
            [
                ("scale_1", 10),
                ("scale_3", 9),
                ("scale_2", 8),
                ("scale_6", 8),
            ],
            [
                ("scale_1", 7),
                ("scale_2", 7),
                ("scale_3", 7),
                ("scale_4", 7),
                ("scale_5", 7),
                ("scale_6", 7),
            ],
        ]
        for test_name, expected in zip(test_scale_scores_counters, expected):
            with self.subTest(test_name=test_name):
                received = task_3._make_top_scales_by_scores(
                    test_scale_scores_counters[test_name]
                )
                self.assertEquals(received, expected)

    def test_write_result_to_string(self):
        """Проверяет корректность формирования результирующей строки."""
        top_scores_scale = [("scale_3", 10), ("scale_1", 9), ("scale_5", 8)]
        expected = "scale_3:10 scale_1:9 scale_5:8"
        received = task_3._write_result_to_string(top_scores_scale)
        self.assertEquals(received, expected)
