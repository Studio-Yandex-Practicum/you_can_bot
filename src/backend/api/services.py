from .constants import TEST_2_RESULTS
from .models import Answer


def calculate_test_2_result(user_answers: list[Answer]) -> str:
    """
    Принимает список ответов пользователя на 2 задание,
    расчитывает результат и возвращает описание психотипа.
    """
    ANSWERS_GROUPS_COUNT = 7
    PSYCHO_FEATURES = ('EI', 'SN', 'TF', 'JP')
    MAX_SCORE_BY_FEATURE = (10, 20, 20, 20)

    answers_groups = [[] for _ in range(ANSWERS_GROUPS_COUNT)]
    for answer in user_answers:
        answers_groups[answer.number % 7 - 1].append(1 if answer.content == 'а' else 0)

    user_letter_a_score_by_feature = (
        sum(answers_groups[0]),
        sum(answers_groups[1] + answers_groups[2]),
        sum(answers_groups[3] + answers_groups[4]),
        sum(answers_groups[5] + answers_groups[6]),
    )
    user_psychotype = ''.join(
        [
            features[0 if a_result > max_score / 2 else 1]
            for features, max_score, a_result
            in zip(
                PSYCHO_FEATURES,
                MAX_SCORE_BY_FEATURE,
                user_letter_a_score_by_feature
            )
        ]
    )
    return TEST_2_RESULTS[user_psychotype]
