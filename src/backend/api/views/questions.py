from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from api.models import Task
from api.serializers import QuestionSerializer


@api_view(("GET",))
def get_question(request, task_number, question_number):
    """Получение оформленного сообщения Question."""
    task = _get_task_or_404(task_number)
    questions = _get_questions_or_404(question_number, task)
    serializer = QuestionSerializer(
        questions,
        context={
            "request": request,
            "task_number": task.number,
        },
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


def _get_questions_or_404(number, task):
    questions = task.questions.filter(number=number)
    if not questions:
        raise NotFound(detail=settings.NOT_FOUND_QUESTION_ERROR_MESSAGE)
    return questions


def _get_task_or_404(task_number):
    """Проверка отсутствия/существования Задания."""
    try:
        task = Task.objects.get(number=task_number)
    except Task.DoesNotExist:
        raise NotFound(detail=settings.NOT_FOUND_TASK_ERROR_MESSAGE)
    return task
