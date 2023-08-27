from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

from .models import UserFromTelegram
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
    lookup_field = "number"

    def get_queryset(self):
        user = get_object_or_404(
            UserFromTelegram, telegram_id=self.kwargs.get("telegram_id")
        )
        if not self.kwargs.get("number"):
            return user.tasks.objects.all()
        return user.tasks.objects.filter(user=self.kwargs.get("number"))

    def get_serializer_class(self):
        if self.action == "list":
            return TaskStatusRetriveSerializer
        return TaskStatusListSerializer
