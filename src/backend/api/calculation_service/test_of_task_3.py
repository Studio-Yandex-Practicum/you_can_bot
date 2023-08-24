from random import shuffle, sample
from collections import namedtuple

from django.test import TestCase

from api.calculation_service.task_3 import calculate_task_3_result
from api.models import Answer


class TestTask3(TestCase):

    SCALES_ANSWERS = {
        'scale_1': (
            '1а', '2а', '3а', '4а', '5а', '16а', '17а', '19а',
            '21а', '28а', '31а', '32а', '33а', '34а'),
        'scale_2': (
            '1б', '6а', '7а', '8а', '9а', '16б', '20а', '22а',
            '23а', '24а', '31б', '35а', '36а', '37а'),
        'scale_3': (
            '2б', '6б', '10а', '11а', '12а', '17б', '20б',
            '25а', '26а', '27а', '36б', '38а', '39а', '41б'),
        'scale_4': (
            '3б', '7б', '10б', '13а', '14а', '18а', '19б',
            '22б', '29а', '32б', '35б', '38б', '40а', '42а'),
        'scale_5': (
            '4б', '8б', '11б', '13б', '15а', '18б', '23б',
            '25б', '26б', '28б', '30а', '33б', '39б', '40б'),
        'scale_6': (
            '5б', '9б', '12б', '14б', '15б', '21б', '24б',
            '27б', '29б', '30б', '34б', '37б', '41а', '42б'),
        }

    def test_task_3_calculation(self):
        """
        Тестирует различные сценарии распределения ответов между шкалами,
        применяя указанное распределение баллов к рандомно выбранным шкалам
        и генеря соответствующее кол-во рандомных ответов для этих шкал.
        """
        TestData = namedtuple(
            'TestData', ['answers_split_between_scales', 'leaders_count', 'error']
        )
        SPLITS_FOR_TESTS = (
            TestData(
                (10, 9, 8, 6, 5, 4), 3,
                'Ошибка в тесте c 3 четкими лидерами'),
            TestData(
                (10, 9, 8, 8, 4, 3), 4,
                'Ошибка в тесте с одинаковым баллом за 3-4 места'),
            TestData(
                (7, 7, 7, 7, 7, 7), 6,
                'Ошибка в тесте с одинаковым баллом по всем шкалам'),
            TestData(
                (14, 14, 14, 0, 0, 0), 3,
                'Ошибка в тесте со шкалами с 0'),
        )
        for split in SPLITS_FOR_TESTS:
            field = split.answers_split_between_scales
            with self.subTest(field=field):
                expected_scales_with_scores = self._generate_scales_and_scores_pairs(
                    split.answers_split_between_scales
                )
                user_answers = self._generate_user_answers(
                    expected_scales_with_scores
                )
                received_response = calculate_task_3_result(user_answers)
                expected_response = (' ').join(
                    [
                        (':').join([scale, str(score)])
                        for scale, score
                        in expected_scales_with_scores[:split.leaders_count]
                    ]
                )
            self.assertEquals(received_response, expected_response, split.error)

    def _generate_scales_and_scores_pairs(
        self, split_between_scales: tuple[int]
    ) -> list[tuple[str, int]]:
        """
        Присваивает заданное распределение баллов рандомным шкалам.
        Такое кол-во ответов по каждой шкале нужно будет сгенерировать далее.
        """
        shuffled_scales = list(self.SCALES_ANSWERS)
        shuffle(shuffled_scales)
        scales_with_scores = list(zip(shuffled_scales, split_between_scales))
        return sorted(scales_with_scores, key=lambda pair: (-pair[1], pair[0]))

    def _generate_user_answers(self, scales_with_scores) -> list[Answer]:
        """
        Создает список случайных ответов так, чтобы кол-во ответов,
        относящихся к каждой шкале, соответствовало баллам
        той же шкалы в scales_with_scores.
        """
        user_answers = []
        for scale, answers_quantity in scales_with_scores:
            current_scale_user_answers = map(
                lambda answer: Answer(number=int(answer[:-1]), content=(answer[-1])),
                sample(self.SCALES_ANSWERS[scale], answers_quantity)
            )
            user_answers.extend(current_scale_user_answers)
        return user_answers
