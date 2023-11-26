import asyncio

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.conversation_utils import non_context_send_message
from api.models import UserFromTelegram
from api.serializers import ProblemSerializer
from backend.settings import MAIN_MENTOR_ID

PROBLEM_TEXT = "Пользователь {user} отправил вопрос: «{question}»"


@api_view(("POST",))
def problem_create(request, telegram_id):
    """
    Создание записи в таблице Problem.
    """
    user = get_object_or_404(UserFromTelegram, telegram_id=telegram_id)
    serializer = ProblemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        try:
            mentor_id_of_user = user.mentor.telegram_id
            if mentor_id_of_user is None:
                mentor_id_of_user = MAIN_MENTOR_ID
        except AttributeError as err:
            if str(err) == "'NoneType' object has no attribute 'telegram_id'":
                mentor_id_of_user = MAIN_MENTOR_ID
            else:
                raise AttributeError
        asyncio.run(
            non_context_send_message(
                text=PROBLEM_TEXT.format(
                    user=f"{user.name} {user.surname}",
                    question=serializer.data["message"],
                ),
                user_id=mentor_id_of_user,
            )
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
