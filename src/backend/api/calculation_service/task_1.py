import logging
import re
from typing import Tuple

from rest_framework.serializers import ValidationError

from api.models import Answer, ResultStatus, Result

_LOGGER = logging.getLogger(__name__)

LETTERS: tuple[str, ...] = ("А", "Б", "В", "Г", "Д", "Е")
ANSWER_OPTIONS_COUNT: int = 6


def calculate_task_1_result(user_answers: list[Answer]) -> str:
    """
    Принимает список ответов по первому заданию, и возвращает буквы,
    относящиеся к расшифровке трех профессиональных склонностей человека по
    результатам ответов на вопросы из первого теста.
    """
    results = _get_result_points(user_answers)
    # Формируем summary из трех результатов, набравших больше всего баллов.
    summary = [f"{result[1]};{result[0]}" for result in results[:3]]

    # Если третье место делят несколько качеств, записываем их тоже.
    third_place_scores = results[2][0]

    for result in results[3:]:
        if result[0] == third_place_scores:
            summary.append(f"{result[1]};{result[0]}")
        else:
            break

    return "\n".join(summary)


def calculate_task_1_result_to_db(user_answers: list[Answer]) -> None:
    """
    Принимает список ответов по первому заданию, рассчитывает результат и
    создает запись в базе данных ResultStatus.
    """
    results = _get_result_points(user_answers)
    task_status = user_answers[0].task_status

    # Очистка базы данных от предыдущих результатов ResultStatus.
    task_status.result.all().delete()

    # Создание в базе данных новых результатов ResultStatus.
    result_status = (
        ResultStatus(
            task_status=task_status,
            top=results.index(result) + 1,
            result=Result.objects.get(task=task_status.task, key=result[1]),
            score=result[0])
        for result in results if
        results.index(result) < 3 or result[0] == results[2][0]
    )
    ResultStatus.objects.bulk_create(result_status)


def _validate_answer(answer: Answer) -> None:
    """Проверяет поле Answer.content на консистентность данных."""
    if answer.content is None or not re.match("[0-5]{6}", answer.content):
        error_message = (
            "Строка Answer.content Задания 1 должна содержать только цифры от"
            f"0 до 5 длиной {ANSWER_OPTIONS_COUNT} строки,"
            f" ID ответа: {answer.id}"
        )
        _LOGGER.error(error_message)
        raise ValidationError({"errors": error_message})


def _get_result_points(user_answers: list[Answer]) -> list[Tuple[int, str]]:
    points = [0] * ANSWER_OPTIONS_COUNT

    for answer in user_answers:
        _validate_answer(answer)
        answer_points = tuple(map(int, answer.content))
        for index, value in enumerate(answer_points):
            points[index] += value
    return sorted(zip(points, LETTERS), reverse=True)
