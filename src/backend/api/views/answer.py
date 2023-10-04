from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from api.calculation_service.task_1 import calculate_task_1_result
from api.calculation_service.task_2 import calculate_task_2_result
from api.calculation_service.task_3 import calculate_task_3_result
from api.calculation_service.task_4 import calculate_task_4_result
from api.models import Answer, Question, TaskStatus
from api.serializers import AnswerSerializer

ANSWER_CREATE_ERROR = "Ошибка при обработке запроса: {error}"
CALCULATE_TASKS = {
    1: calculate_task_1_result,
    2: calculate_task_2_result,
    3: calculate_task_3_result,
    4: calculate_task_4_result,
}


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
        if task_status.current_question == task_status.task.end_question:
            _create_result_status(
                task_status, task_number, task_status.task.end_question
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def _get_question_or_404(number, task_number):
    try:
        question = Question.objects.get(task__number=task_number, number=number)
    except Question.DoesNotExist:
        raise NotFound(detail=settings.NOT_FOUND_QUESTION_ERROR_MESSAGE)
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


def _create_result_status(task_status, task_number, end_question):
    answers = _check_all_answers_exist(task_status, end_question)
    task_status.is_done = True
    task_status.pass_date = timezone.now()
    task_status.save()
    CALCULATE_TASKS.get(task_number)(answers)


def _check_all_answers_exist(task_status, end_question):
    user_answers = set(task_status.answers.values_list("question__number", flat=True))
    if len(user_answers) != end_question:
        not_exist_answers = set(range(1, end_question + 1)) - user_answers
        raise NotFound(
            detail="Нет полученных ответов на вопросы с номерами: "
            f"{', '.join(map(str, not_exist_answers))}"
        )
    return task_status.answers.all()
