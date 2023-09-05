from api.models import Answer

SCALES = {
    "1а": "scale_1",
    "1б": "scale_2",
    "2а": "scale_1",
    "2б": "scale_3",
    "3а": "scale_1",
    "3б": "scale_4",
    "4а": "scale_1",
    "4б": "scale_5",
    "5а": "scale_1",
    "5б": "scale_6",
    "6а": "scale_2",
    "6б": "scale_3",
    "7а": "scale_2",
    "7б": "scale_4",
    "8а": "scale_2",
    "8б": "scale_5",
    "9а": "scale_2",
    "9б": "scale_6",
    "10а": "scale_3",
    "10б": "scale_4",
    "11а": "scale_3",
    "11б": "scale_5",
    "12а": "scale_3",
    "12б": "scale_6",
    "13а": "scale_4",
    "13б": "scale_5",
    "14а": "scale_4",
    "14б": "scale_6",
    "15а": "scale_5",
    "15б": "scale_6",
    "16а": "scale_1",
    "16б": "scale_2",
    "17а": "scale_1",
    "17б": "scale_3",
    "18а": "scale_4",
    "18б": "scale_5",
    "19а": "scale_1",
    "19б": "scale_4",
    "20а": "scale_2",
    "20б": "scale_3",
    "21а": "scale_1",
    "21б": "scale_6",
    "22а": "scale_2",
    "22б": "scale_4",
    "23а": "scale_2",
    "23б": "scale_5",
    "24а": "scale_2",
    "24б": "scale_6",
    "25а": "scale_3",
    "25б": "scale_5",
    "26а": "scale_3",
    "26б": "scale_5",
    "27а": "scale_3",
    "27б": "scale_6",
    "28а": "scale_1",
    "28б": "scale_5",
    "29а": "scale_4",
    "29б": "scale_6",
    "30а": "scale_5",
    "30б": "scale_6",
    "31а": "scale_1",
    "31б": "scale_2",
    "32а": "scale_1",
    "32б": "scale_4",
    "33а": "scale_1",
    "33б": "scale_5",
    "34а": "scale_1",
    "34б": "scale_6",
    "35а": "scale_2",
    "35б": "scale_4",
    "36а": "scale_2",
    "36б": "scale_3",
    "37а": "scale_2",
    "37б": "scale_6",
    "38а": "scale_3",
    "38б": "scale_4",
    "39а": "scale_3",
    "39б": "scale_5",
    "40а": "scale_4",
    "40б": "scale_5",
    "41а": "scale_6",
    "41б": "scale_3",
    "42а": "scale_4",
    "42б": "scale_6",
}
TOP_RESULTS_NUMBER = 3


def calculate_task_3_result(user_answers: list[Answer]) -> str:
    """
    Принимает список ответов пользователя на 3 задание,
    расчитывает результат и возвращает топ 3 характеристики,
    наиболее подходящие пользователю.
    """
    scale_scores_counter = _distribute_answers_by_scales(user_answers)
    scale_scores_sorted = _sorted_scales_in_non_growing_order(scale_scores_counter)
    user_top_features = _make_top_scales_by_scores(scale_scores_sorted)
    summary = _write_result_to_string(user_top_features)
    return summary


def _distribute_answers_by_scales(user_answers: list[Answer]) -> dict[str:int]:
    """
    Считает кол-во ответов пользователя, относящихся к каждой из шкал.
    """
    scale_scores_counter = {}
    for answer in user_answers:
        scale = SCALES[str(answer.number) + answer.content]
        scale_scores_counter[scale] = scale_scores_counter.get(scale, 0) + 1
    return scale_scores_counter


def _sorted_scales_in_non_growing_order(
    scale_scores_counter: dict[str:int],
) -> list[tuple[str, int]]:
    """
    Сортирует шкалы и кол-во ответов, относящихся к ним, по невозрастанию.
    """
    return sorted(
        scale_scores_counter.items(),
        key=lambda scale_item: (-scale_item[1], scale_item[0]),
    )


def _make_top_scales_by_scores(
    scale_scores_sorted: list[tuple[str, int]]
) -> list[tuple[str, int]]:
    """
    Выбирает шкалы (топ-3), набравшие максимальное кол-во баллов.
    В случае, если шкалы, не вошедшие в топ-3, набрали столько же баллов,
    что и шкала на 3 месте, добавляет их в выборку.
    """
    user_top_features = scale_scores_sorted[:TOP_RESULTS_NUMBER]
    for scale, score in scale_scores_sorted[TOP_RESULTS_NUMBER:]:
        if score != user_top_features[-1][-1]:
            return user_top_features
        user_top_features.append((scale, score))
    return user_top_features


def _write_result_to_string(user_top_features: list[tuple[str, int]]) -> str:
    """Формирует результат в виде текстовой строки."""
    return " ".join(
        [":".join([scale, str(score)]) for scale, score in user_top_features]
    )
