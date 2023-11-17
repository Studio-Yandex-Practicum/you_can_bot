from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotAcceptable, NotFound
from rest_framework.response import Response

from api.models import TaskStatus, UserFromTelegram
from api.serializers import AnswerSerializer, TaskResultsForUserSerializer

USER_404 = "Пользователь не найден."
TASK_404 = "Задание не найдено."
TASK_NOT_COMPLETED = "Ошибка! Задание не завершено."


@api_view(("GET",))
def get_results_for_user_by_task(request, telegram_id, task_number):
    """
    Получение результата выполнения конкретного задания
    конкретным пользователем.
    """
    try:
        user = UserFromTelegram.objects.get(telegram_id=telegram_id)
    except UserFromTelegram.DoesNotExist:
        raise NotFound(USER_404)
    try:
        task_status = user.tasks.get(task__number=task_number)
        if not task_status.is_done:
            raise NotAcceptable(TASK_NOT_COMPLETED)
    except TaskStatus.DoesNotExist:
        raise NotFound(TASK_404)

    if task_number in (5, 6, 7):
        answers = task_status.answers.all()
        serializer = AnswerSerializer(answers, context={"as_result": True})
        return Response(serializer.data, status=status.HTTP_200_OK)

    results = task_status.result.all()
    serializer = TaskResultsForUserSerializer(
        results, context={"request": request, "task_number": task_number}
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
