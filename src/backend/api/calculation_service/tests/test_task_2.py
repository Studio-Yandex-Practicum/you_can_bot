from django.test import TestCase

from api.calculation_service.task_2 import _get_result
from api.models import Answer, Question, Task, TaskStatus, UserFromTelegram


class TestTask2(TestCase):
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
            task__number=2,
        )

    def setUp(self) -> None:
        questions = [
            Question(task=Task.objects.get(number=2), number=question_number)
            for question_number in range(1, 71)
        ]
        Question.objects.bulk_create(questions)
        answers = [
            Answer(task_status=self.task_status, question=question, content="б")
            for question in questions
        ]
        Answer.objects.bulk_create(answers)
        self.user_answers = Answer.objects.filter(task_status=self.task_status)

    def test_e_psycho_feature_is_defined_correctly(self):
        answers_for_e_feature = (1, 8, 15, 22, 29, 36, 43, 50, 57, 64)
        for index, number_of_answer in enumerate(answers_for_e_feature):
            self._change_answer_content(number_of_answer)
            answers_with_letter_a = index + 1
            with self.subTest(anwers_with_letter_a=answers_with_letter_a):
                received_response = _get_result(user_answers=self.user_answers.all())[0]
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
            self._change_answer_content(number_of_answer)
            answers_with_letter_a = index + 1
            with self.subTest(anwers_with_letter_a=answers_with_letter_a):
                received_response = _get_result(user_answers=self.user_answers.all())[1]
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
            self._change_answer_content(number_of_answer)
            answers_with_letter_a = index + 1
            with self.subTest(anwers_with_letter_a=answers_with_letter_a):
                received_response = _get_result(user_answers=self.user_answers.all())[2]
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
            self._change_answer_content(number_of_answer)
            answers_with_letter_a = index + 1
            with self.subTest(anwers_with_letter_a=answers_with_letter_a):
                received_response = _get_result(user_answers=self.user_answers.all())[3]
                if answers_with_letter_a >= 11:
                    expected_response = "J"
                else:
                    expected_response = "P"
                self.assertEquals(received_response, expected_response)

    def _change_answer_content(self, number_of_answer, new_content="а"):
        answer = self.user_answers.get(question__number=number_of_answer)
        answer.content = new_content
        answer.save()
