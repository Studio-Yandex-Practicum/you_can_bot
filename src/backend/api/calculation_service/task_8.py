from api.models import Answer, Result, ResultStatus


def calculate_task_8_result(user_answers: list[Answer]) -> None:
    answer = user_answers[0]
    results = answer.content.split(",")
    task_status = answer.task_status
    task_status.result.all().delete()
    result_statuses = (
        ResultStatus(
            task_status=task_status,
            result=Result.objects.get(task=task_status.task, key=result),
            top=top,
        )
        for top, result in enumerate(results, start=1)
    )
    ResultStatus.objects.bulk_create(result_statuses)
