from api.models import Answer, Result, ResultStatus

SCALES = {
    "1": [1, 9, 17, 25, 33],
    "2": [2, 10, 18, 26, 34],
    "3": [3, 11, 19, 27, 35],
    "4": [4, 12, 36],
    "5": [20, 28, 41],
    "6": [5, 13, 21, 29, 37],
    "7": [6, 14, 22, 30, 38],
    "8": [7, 15, 23, 31, 39],
    "9": [8, 16, 24, 32, 40],
}
MIN_AVG_SCORE = 6


def calculate_task_4_result(user_answers: list[Answer]) -> None:
    user_answers_dict = _transform_answers_to_dict(user_answers)
    scales_avg_score = _calculate_scales_avg_score(user_answers_dict)
    results = _get_top_features_sorted(scales_avg_score)
    if results:
        task_status = user_answers[0].task_status

        # Очистка базы данных от предыдущих результатов ResultStatus.
        task_status.result.all().delete()

        # Создание в базе данных новых результатов ResultStatus.
        result_status = (
            ResultStatus(
                task_status=task_status,
                top=results.index(result) + 1,
                result=Result.objects.get(task=task_status.task, key=result[0]),
                score=result[1],
            )
            for result in results
        )
        ResultStatus.objects.bulk_create(result_status)


def _transform_answers_to_dict(user_answers: list[Answer]) -> dict[int:int]:
    return {int(answer.question.number): int(answer.content) for answer in user_answers}


def _calculate_scales_avg_score(user_answers: dict[int:int]) -> dict[str:float]:
    scales_avg_score = {}
    for scale, questions in SCALES.items():
        scale_total_score = sum(user_answers[question] for question in questions)
        scales_avg_score[scale] = scale_total_score / len(SCALES[scale])
    return scales_avg_score


def _get_top_features_sorted(scales_avg_score: dict[str:float]) -> list[str]:
    sorted_scales = sorted(
        scales_avg_score.items(), key=lambda scale: (-scale[1], scale[0])
    )
    filtered_scales = [scale for scale in sorted_scales if scale[1] > MIN_AVG_SCORE]
    return filtered_scales
