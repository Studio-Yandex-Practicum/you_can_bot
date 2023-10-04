from rest_framework.test import APITestCase

from api.models import Question, Result, Task, TaskStatus, UserFromTelegram


class BaseCaseForAnswerTests(APITestCase):
    """Базовый набор констант для тестов модуля api."""

    TELEGRAM_ID = 1234567
    TELEGRAM_USERNAME = "hasnoname"
    TELEGRAM_NAME = "HasNoName"
    TELEGRAM_SURNAME = "HasNoSurname"
    TASK_NUMBER_1 = 1
    TASK_NUMBER_2 = 2
    TASK_NUMBER_3 = 3
    TASK_NUMBER_4 = 4

    # Количество заданий, изменить при добавлении заданий в тесты
    TASK_COUNT = 4

    TASK_NUMBER_99 = 99
    ANSWER_1 = {"number": "1", "content": "a"}
    ANSWER_2 = {"number": 1, "content": "б"}
    ANSWER_3 = {"number": "first", "content": "б"}
    ANSWER_4 = {"number": 2, "content": "a"}
    ANSWER_5 = {"number": 1}

    # Key для формирования результатов Results, при добавлении Заданий дополнить
    # fmt: off
    TASKS_KEYS = {
        1: ("А", "Б", "В", "Г", "Д", "Е",),
        2: ("ESFP", "ISFP", "ESTP", "ISTP", "ESFJ", "ISFJ", "ESTJ", "ISTJ",
            "ENFJ", "INFJ", "ENFP", "INFP", "ENTJ", "INTJ", "ENTP", "INTP",),
        3: ("scale_1", "scale_2", "scale_3", "scale_4", "scale_5", "scale_6",),
        4: ("1", "2", "3", "4", "5", "6", "7", "8", "9",)
    }
    # fmt: on

    # Константы для Задания №1
    TASK1_ANSWERS_CONTENT = {
        1: "543210",
        2: "053142",
        3: "123504",
        4: "041235",
        5: "012345",
        6: "410523",
        7: "321054",
        8: "013245",
        9: "543012",
        10: "230451",
    }
    RESULT_KEY_TASK_1 = "Е"
    RESULT_TOP_TASK_1 = 1
    RESULT_SCORE_TASK_1 = 31

    # Константы для Задания №2
    RESULT_KEY_TASK_2 = "INFP"
    RESULT_TOP_TASK_2 = 1

    # Константы для Задания №3
    RESULT_KEY_TASK_3 = "scale_6"
    RESULT_TOP_TASK_3 = 1
    RESULT_SCORE_TASK_3 = 13

    # Константы для Задания №4
    # fmt: off
    TASK4_ANSWERS_CONTENT = {
        1: 6, 2: 4, 3: 9, 4: 1, 5: 10, 6: 6, 7: 9, 8: 7, 9: 10, 10: 8,
        11: 4, 12: 2, 13: 6, 14: 4, 15: 5, 16: 6, 17: 7, 18: 8, 19: 9,
        20: 5, 21: 4, 22: 1, 23: 10, 24: 7, 25: 5, 26: 7, 27: 3, 28: 4,
        29: 2, 30: 6, 31: 1, 32: 9, 33: 6, 34: 8, 35: 10, 36: 3, 37: 5,
        38: 6, 39: 3, 40: 9, 41: 6
    }
    # fmt: on
    RESULT_KEY_TASK_4 = "9"
    RESULT_TOP_TASK_4 = 1
    RESULT_SCORE_TASK_4 = 7

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_from_telegram = UserFromTelegram.objects.create(
            telegram_id=cls.TELEGRAM_ID,
            telegram_username=cls.TELEGRAM_USERNAME,
            name=cls.TELEGRAM_NAME,
            surname=cls.TELEGRAM_SURNAME,
        )

        tasks = {
            task_number: Task.objects.get(number=task_number)
            for task_number in range(1, cls.TASK_COUNT + 1)
        }
        cls.tasks_status = {
            task_number: TaskStatus.objects.get(
                user=cls.user_from_telegram, task__number=task_number
            )
            for task_number in range(1, cls.TASK_COUNT + 1)
        }

        questions = []
        for task_number in range(1, cls.TASK_COUNT + 1):
            for num in range(1, tasks[task_number].end_question + 1):
                questions.append(
                    Question(
                        task=tasks[task_number],
                        number=num,
                        content=f"Вопрос_{num}",
                        example="",
                    )
                )
        Question.objects.bulk_create(questions)

        results = []
        for task_number in range(1, cls.TASK_COUNT + 1):
            for key in cls.TASKS_KEYS[task_number]:
                results.append(
                    Result(task=tasks[task_number], key=key, title="", description="")
                )
        Result.objects.bulk_create(results)
