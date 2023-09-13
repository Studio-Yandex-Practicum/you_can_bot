from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, NotAcceptable
from rest_framework.response import Response

from api.models import UserFromTelegram, Task, ResultStatus, TaskStatus
from api.serializers import TaskResultsForUserSerializer

USER_404 = "Пользователь не найден."
TASK_404 = "Задание не найдено."
TASK_NOT_COMPLETED = "Ошибка! Задание не завершено."


@api_view(('GET',))
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
        task = Task.objects.get(number=task_number)
    except Task.DoesNotExist:
        raise NotFound(TASK_404)
    if not TaskStatus.objects.get(user=user, task=task).is_done:
        raise NotAcceptable(TASK_NOT_COMPLETED)

    results = ResultStatus.objects.filter(
        task_status__task=task,
        task_status__user=user
    )

    serializer = TaskResultsForUserSerializer(
        results,
        context={'request': request}
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
