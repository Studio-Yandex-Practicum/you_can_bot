from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from api.models import Answer, Question, TaskStatus
from api.serializers import AnswerSerializer

ANSWER_CREATE_ERROR = "Ошибка при обработке запроса: {error}"


@api_view(("POST",))
def answer_create(request, telegram_id, task_number):
    """
    Создание записи в таблице Answer.
    Изменение в таблице TaskStatus поля current_question для пользователя.
    """
    task_status = _get_task_status_or_404(task_number, telegram_id)
    number = _get_and_validate_number_of_question(request)
    question = _get_question_or_404(number, task_number)
    answer = task_status.answers.filter(question=question)
    if answer.exists() and request.data.get("content"):
        serializer = AnswerSerializer(answer.first(), data=request.data, partial=True)
    else:
        serializer = AnswerSerializer(
            Answer(task_status=task_status, question=question), data=request.data
        )
    if serializer.is_valid():
        serializer.save()
        if task_status.current_question < number:
            task_status.current_question = number
            task_status.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def _get_question_or_404(number, task_number):
    try:
        question = Question.objects.get(task__number=task_number, number=number)
    except Question.DoesNotExist:
        raise NotFound(detail="Не найден вопрос с таким номером.")
    return question


def _get_and_validate_number_of_question(request):
    try:
        number = int(request.data.get("number"))
    except ValueError as error:
        raise ValidationError(detail=ANSWER_CREATE_ERROR.format(error=error))
    return number


def _get_task_status_or_404(task_number, telegram_id):
    try:
        task_status = TaskStatus.objects.get(
            user__telegram_id=telegram_id, task__number=task_number
        )
    except TaskStatus.DoesNotExist:
        raise NotFound(
            detail="Не найдена связка задания и пользователя."
            " Возможно неверно указаны telegram_id и task_number."
        )
    return task_status
