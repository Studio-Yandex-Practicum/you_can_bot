from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from api.models import UserFromTelegram
from api.serializers import TaskStatusSerializer, TaskStatusRetrieveSerializer


class TasksViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    Вьюсет для получения информации о всех заданиях пользователя и
    получения информации о статусе выполнения конкретного задания.
    Доступные HTTP методы: GET
    """

    http_method_names = ["get"]
    lookup_field = "task__number"

    def get_queryset(self):
        user = get_object_or_404(
            UserFromTelegram, telegram_id=self.kwargs.get("telegram_id")
        )
        return user.tasks.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TaskStatusSerializer
        return TaskStatusRetrieveSerializer
