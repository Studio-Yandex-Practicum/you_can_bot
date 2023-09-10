from api.models import UserFromTelegram, Task, ResultStatus
from api.serializers import TaskResultsForUserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

USER_404 = "Пользователь не найден."
TASK_404 = "Задание не найдено."


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
    results = ResultStatus.objects.filter(
        task_status__task=task,
        task_status__user=user
    )
    serializer = TaskResultsForUserSerializer(
        results,
        context={'request': request}
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
