from api.models import Answer

LETTERS: tuple[str, ...] = ('А', 'Б', 'В', 'Г', 'Д', 'Е')
ANSWER_OPTIONS_COUNT: int = 6


def calculate_task_1_result(user_answers: list[Answer]) -> str:
    """
    Принимает список ответов по первому заданию, и возвращает буквы,
    относящиеся к расшифровке трех профессиональных склонностей человека по
    результатам ответов на вопросы из первого теста.
    """
    points = [0] * ANSWER_OPTIONS_COUNT

    for answer in user_answers:
        answer_points = list(map(int, answer.content))
        points = [
            points[idx] + answer_points[idx]
            for idx in range(len(answer_points))
        ]

    results = sorted(zip(points, LETTERS))[::-1]
    summary = [result[1] for result in results[:3]]
    return ''.join(summary)
