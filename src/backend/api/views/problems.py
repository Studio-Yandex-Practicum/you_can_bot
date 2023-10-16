import asyncio
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import UserFromTelegram
from api.serializers import ProblemSerializer
from ..conversation_utils import non_context_send_message
from backend.settings import MAIN_MENTOR_ID

PROBLEM_TEXT = "Пользователь {user} отправил вопрос: «{question}»."


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
            user_id = user.mentor.telegram_id
        except AttributeError as err:
            if str(err) == "'NoneType' object has no attribute 'telegram_id'":
                user_id = MAIN_MENTOR_ID
        asyncio.run(
            non_context_send_message(
                text=PROBLEM_TEXT.format(
                    user=user.name, question=serializer.data["message"]
                ),
                user_id=user_id,
            )
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
