from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import TaskStatus, UserFromTelegram
from api.serializers import (
    AnswerSerializer,
    TaskStatusListSerializer,
    TaskStatusRetriveSerializer,
    UserFromTelegramRetrieveCreateSerializer,
    UserFromTelegramUpdateSerializer,
)

ANSWER_CREATE_ERROR = "Ошибка при обработке запроса: {error}"


@api_view(("POST",))
def answer_create(request, telegram_id, task_number):
    """
    Создание записи в таблице Answer.
    Изменение в таблице TaskStatus поля current_question для пользователя.
    """
    user = get_object_or_404(UserFromTelegram, telegram_id=telegram_id)
    task = get_object_or_404(TaskStatus, user=user, number=task_number)
    try:
        number = int(request.data.get("number"))
    except ValueError as error:
        return Response(
            ANSWER_CREATE_ERROR.format(error=error), status=status.HTTP_400_BAD_REQUEST
        )
    request.data["task"] = task_number
    answers = task.answers.filter(number=number)
    if answers.exists() and request.data.get("content"):
        serializer = AnswerSerializer(answers.first(), data=request.data, partial=True)
    else:
        serializer = AnswerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        if task.current_question < number:
            task.current_question = number
            task.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFromTelegramViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Вьюсет для обработки запросов, связанных с пользователем telegram.
    Доступные HTTP методы: GET, POST, PATCH.
    Поле для detail-запросов: telegram_id.
    """

    queryset = UserFromTelegram.objects.all()
    http_method_names = ["get", "post", "patch"]
    lookup_field = "telegram_id"

    def get_serializer_class(self):
        if self.action == "partial_update":
            return UserFromTelegramUpdateSerializer
        return UserFromTelegramRetrieveCreateSerializer


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
        return user.tasks.all()

    def get_serializer_class(self):
        if self.action == "list":
            return TaskStatusListSerializer
        return TaskStatusRetriveSerializer
