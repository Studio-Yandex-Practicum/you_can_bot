from django.test import TestCase

from api.calculation_service.task_2 import calculate_task_2_result
from api.models import Answer


class TestTask2(TestCase):
    def setUp(self) -> None:
        self.user_answers = [
            Answer(content="б", number=number) for number in range(1, 71)
        ]

    def test_e_psycho_feature_is_defined_correctly(self):
        answers_for_e_feature = (1, 8, 15, 22, 29, 36, 43, 50, 57, 64)
        for index, number_of_answer in enumerate(answers_for_e_feature):
            self.user_answers[number_of_answer - 1] = Answer(
                content="а", number=number_of_answer
            )
            answers_with_letter_a = index + 1
            with self.subTest(anwers_with_letter_a=answers_with_letter_a):
                received_response = calculate_task_2_result(
                    user_answers=self.user_answers
                )[0]
                if answers_with_letter_a >= 6:
                    expected_response = "E"
                else:
                    expected_response = "I"
                self.assertEquals(received_response, expected_response)

    def test_s_psycho_feature_is_defined_correctly(self):
        answers_for_s_feature = (
            2,
            3,
            9,
            10,
            16,
            17,
            23,
            24,
            30,
            31,
            37,
            38,
            44,
            45,
            51,
            52,
            58,
            59,
            65,
            66,
        )
        for index, number_of_answer in enumerate(answers_for_s_feature):
            self.user_answers[number_of_answer - 1] = Answer(
                content="а", number=number_of_answer
            )
            answers_with_letter_a = index + 1
            with self.subTest(anwers_with_letter_a=answers_with_letter_a):
                received_response = calculate_task_2_result(
                    user_answers=self.user_answers
                )[1]
                if answers_with_letter_a >= 11:
                    expected_response = "S"
                else:
                    expected_response = "N"
                self.assertEquals(received_response, expected_response)

    def test_t_psycho_feature_is_defined_correctly(self):
        answers_for_t_feature = (
            4,
            5,
            11,
            12,
            18,
            19,
            25,
            26,
            32,
            33,
            39,
            40,
            46,
            47,
            53,
            54,
            60,
            61,
            67,
            68,
        )
        for index, number_of_answer in enumerate(answers_for_t_feature):
            self.user_answers[number_of_answer - 1] = Answer(
                content="а", number=number_of_answer
            )
            answers_with_letter_a = index + 1
            with self.subTest(anwers_with_letter_a=answers_with_letter_a):
                received_response = calculate_task_2_result(
                    user_answers=self.user_answers
                )[2]
                if answers_with_letter_a >= 11:
                    expected_response = "T"
                else:
                    expected_response = "F"
                self.assertEquals(received_response, expected_response)

    def test_j_psycho_feature_is_defined_correctly(self):
        answers_for_j_feature = (
            6,
            7,
            13,
            14,
            20,
            21,
            27,
            28,
            34,
            35,
            41,
            42,
            48,
            49,
            55,
            56,
            62,
            63,
            69,
            70,
        )
        for index, number_of_answer in enumerate(answers_for_j_feature):
            self.user_answers[number_of_answer - 1] = Answer(
                content="а", number=number_of_answer
            )
            answers_with_letter_a = index + 1
            with self.subTest(anwers_with_letter_a=answers_with_letter_a):
                received_response = calculate_task_2_result(
                    user_answers=self.user_answers
                )[3]
                if answers_with_letter_a >= 11:
                    expected_response = "J"
                else:
                    expected_response = "P"
                self.assertEquals(received_response, expected_response)
