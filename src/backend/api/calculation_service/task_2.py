from api.models import Answer, Result, ResultStatus

ANSWERS_GROUPS_COUNT = 7
PSYCHO_FEATURES = ("EI", "SN", "TF", "JP")
MAX_SCORE_BY_FEATURE = (10, 20, 20, 20)


def calculate_task_2_result(user_answers: list[Answer]) -> None:
    """
    Принимает список ответов пользователя на 2 задание,
    расчитывает результат и возвращает описание психотипа.
    """
    result = _get_result(user_answers)
    task_status = user_answers[0].task_status

    # Очистка базы данных от предыдущих результатов ResultStatus.
    task_status.result.all().delete()

    # Создание в базе данных ResultStatus.
    ResultStatus.objects.create(
        task_status=task_status,
        result=Result.objects.get(task=task_status.task, key=result),
    )


def _get_result(user_answers: list[Answer]) -> str:
    answers_groups = [[] for _ in range(ANSWERS_GROUPS_COUNT)]
    for answer in user_answers:
        answers_groups[answer.question.number % ANSWERS_GROUPS_COUNT - 1].append(
            1 if answer.content == "а" else 0
        )

    user_letter_a_score_by_feature = (
        sum(answers_groups[0]),
        sum(answers_groups[1] + answers_groups[2]),
        sum(answers_groups[3] + answers_groups[4]),
        sum(answers_groups[5] + answers_groups[6]),
    )

    user_psychotype = "".join(
        [
            features[0 if a_result > max_score / 2 else 1]
            for features, max_score, a_result in zip(
                PSYCHO_FEATURES, MAX_SCORE_BY_FEATURE, user_letter_a_score_by_feature
            )
        ]
    )
    return user_psychotype
