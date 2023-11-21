from django.conf import settings
from django.template.loader import render_to_string
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


@api_view(("GET",))
def get_question_for_task_8(request, question_number):
    """Получение оформленного сообщения Question для 8-го опроса."""
    # [
    #     {"question": 1, "choice": "а"}, {"question": 2, "choice": "б"}
    # ]
    task = Task.objects.get(number=8)
    questions = []
    for value in request.data:
        question = task.questions.get(number=value["question"])
        if value["choice"] == "а":
            questions.append(question.choices.first())
        else:
            questions.append(question.choices.last())

    result = {
        "result": [
            {
                "content": render_to_string(
                    "questions/task_8.html",
                    {"question_number": question_number, "choices": questions},
                )
            }
        ]
    }
    return Response(result, status=status.HTTP_200_OK)


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
