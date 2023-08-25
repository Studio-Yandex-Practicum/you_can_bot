from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import TaskStatus, UserFromTelegram
from .serializers import AnswerSerializer

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
