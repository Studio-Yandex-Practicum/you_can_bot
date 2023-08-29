from api.models import Answer


SCALES = {
    '1': [1, 9, 17, 25, 33],
    '2': [2, 10, 18, 26, 34],
    '3': [3, 11, 19, 27, 35],
    '4': [4, 12, 36],
    '5': [20, 28, 41],
    '6': [5, 13, 21, 29, 37],
    '7': [6, 14, 22, 30, 38],
    '8': [7, 15, 23, 31, 39],
    '9': [8, 16, 24, 32, 40],
}
MIN_AVG_SCORE = 6


def calculate_task_3_result(user_answers: list[Answer]) -> str:
    user_answers = _transform_answers_to_dict(user_answers)
    scales_avg_score = _calculate_scales_avg_score(user_answers)
    user_top_features = _get_top_features_sorted(scales_avg_score)
    summary = _write_result_to_string(user_top_features)
    return summary


def _transform_answers_to_dict(user_answers: list[Answer]) -> dict[int: int]:
    return {
        int(answer.number): int(answer.content)
        for answer in user_answers
    }


def _calculate_scales_avg_score(user_answers: dict[int: int]) -> dict[str: float]:
    scales_avg_score = {}
    for scale, questions in SCALES.items():
        scale_total_score = sum(user_answers[question] for question in questions)
        scales_avg_score[scale] = scale_total_score / len(SCALES[scale])
    return scales_avg_score


def _get_top_features_sorted(scales_avg_score: dict[str: float]) -> list[str]:
    sorted_scales = sorted(
        scales_avg_score.items(),
        key=lambda scale: (-scale[1], scale[0])
    )
    filtered_scales = [
        scale[0]
        for scale in sorted_scales
        if scale[1] > MIN_AVG_SCORE
    ]
    return filtered_scales


def _write_result_to_string(user_top_features: list[str]) -> str:
    if user_top_features:
        return ' '.join(user_top_features)
    return '0'
