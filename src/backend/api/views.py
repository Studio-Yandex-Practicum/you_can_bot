from rest_framework import mixins, viewsets

from .models import TaskStatus
from .serializers import TaskStatusListSerializer, TaskStatusRetriveSerializer


class TasksViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    Вьюсет для получения информации о всех заданиях пользователя и
    получения информации о статусе выполнения конкретного задания.
    Доступные HTTP методы: GET
    """

    http_method_names = ["get"]

    def get_queryset(self):
        if self.request.kwargs.get("task_number"):
            return TaskStatus.objects.filter(
                number=self.request.kwargs.get("task_number")
            )
        return TaskStatus.objects.filter(
            user=self.request.kwargs.get("telegram_id")
        )

    def get_serializer(self, *args, **kwargs):
        if self.request.kwargs.get("task_number"):
            return TaskStatusRetriveSerializer
        return TaskStatusListSerializer
