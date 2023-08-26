import logging

from rest_framework.serializers import ValidationError

from api.models import Answer

LETTERS: tuple[str, ...] = ('А', 'Б', 'В', 'Г', 'Д', 'Е')
ANSWER_OPTIONS_COUNT: int = 6


def _validate_answer(answer: Answer) -> None:
    """Проверяет поле Answer.content на консистентность данных."""
    if answer.content is None or len(answer.content) != ANSWER_OPTIONS_COUNT:
        error_message = (
            f'Размер Answer.content не равен {ANSWER_OPTIONS_COUNT}. '
            f'ID ответа: {answer.id}'
        )
        logging.error(error_message)
        raise ValidationError({'errors': error_message})


def calculate_task_1_result(user_answers: list[Answer]) -> str:
    """
    Принимает список ответов по первому заданию, и возвращает буквы,
    относящиеся к расшифровке трех профессиональных склонностей человека по
    результатам ответов на вопросы из первого теста.
    """
    points = [0] * ANSWER_OPTIONS_COUNT

    for answer in user_answers:
        _validate_answer(answer)
        answer_points = tuple(map(int, answer.content))
        for index, value in enumerate(answer_points):
            points[index] += value

    results = sorted(zip(points, LETTERS), reverse=True)

    # Формируем summary из трех результатов, набравших больше всего баллов.
    summary = [f'{result[1]};{result[0]}' for result in results[:3]]

    # Если третье место делят несколько качеств, записываем их тоже.
    third_place_scores = results[2][0]

    for result in results[3:]:
        if result[0] == third_place_scores:
            summary.append(f'{result[1]};{result[0]}')
        else:
            break

    return '\n'.join(summary)
