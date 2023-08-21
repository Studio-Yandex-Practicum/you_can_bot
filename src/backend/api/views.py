
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Answer, TaskStatus, UserFromTelegram
from .serializers import AnswerSerializer


@api_view(('POST',))
def answer_create(request, telegram_id, task_number):
    """
    Создание записи в таблице Answer.
    Изменение в таблице TaskStatus поля current_question для пользователя.
    """
    user = get_object_or_404(UserFromTelegram, telegram_id=telegram_id)
    if not TaskStatus.objects.filter(user=user, number=task_number).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    number = int(request.data.get('number'))
    request.data['task'] = task_number
    answers = Answer.objects.filter(task=task_number, number=number)
    if answers.exists():
        serializer = AnswerSerializer(answers.first(), data=request.data, partial=True)
    else:
        serializer = AnswerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        task = TaskStatus.objects.get(user=user, number=task_number)
        if task.current_question < number:
            task.current_question = number
            task.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)
