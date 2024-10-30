from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins, viewsets

from api.models import Task, UserFromTelegram
from api.serializers import (
    TaskSerializer,
    TaskStatusRetrieveSerializer,
    TaskStatusSerializer,
)


class TaskStatusViewSet(
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


@method_decorator(cache_page(60 * 60 * 2), "dispatch")
class TaskViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
