from rest_framework.test import APITestCase

from api.models import Question, Result, Task, UserFromTelegram


class BaseCaseForAnswerTests(APITestCase):
    """Базовый набор констант для тестов модуля api."""

    TELEGRAM_ID = 1234567
    TELEGRAM_USERNAME = "hasnoname"
    TELEGRAM_NAME = "HasNoName"
    TELEGRAM_SURNAME = "HasNoSurname"
    TASK_NUMBER_1 = 1
    TASK_NUMBER_99 = 99
    ANSWER_1 = {"number": "1", "content": "a"}
    ANSWER_2 = {"number": 1, "content": "б"}
    ANSWER_3 = {"number": "first", "content": "б"}
    ANSWER_4 = {"number": 2, "content": "a"}
    ANSWER_5 = {"number": 1}

    # Константы для первого задания
    TASK1_ANSWERS_CONTENT = {
        1: "543210", 2: "053142", 3: "123504", 4: "041235", 5: "012345",
        6: "410523", 7: "321054", 8: "013245", 9: "543012", 10: "230451",
    }
    LAST_ANSWER_NUMBER = 10
    KEYS_TASK_1 = "АБВГДЕ"
    RESULT_KEY = "Е"
    RESULT_TOP = 1
    RESULT_SCORE = 31

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_from_telegram = UserFromTelegram.objects.create(
            telegram_id=cls.TELEGRAM_ID,
            telegram_username=cls.TELEGRAM_USERNAME,
            name=cls.TELEGRAM_NAME,
            surname=cls.TELEGRAM_SURNAME,
        )
        task_1 = Task.objects.get(number=1)

        # Вопросы и результаты для первого задания
        questions = (
            Question(
                task=task_1, number=num, content=f"Вопрос_{num}", example=""
            )
            for num in range(1, cls.LAST_ANSWER_NUMBER + 1)

        )
        Question.objects.bulk_create(questions)
        results = (
            Result(task=task_1, key=key, title=f"Вопрос_{key}", description="")
            for key in list(cls.KEYS_TASK_1)
        )
        Result.objects.bulk_create(results)
