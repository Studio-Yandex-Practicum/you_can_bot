from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import UserFromTelegram
from api.serializers import ProblemSerializer


@api_view(("POST",))
def problem_create(request, telegram_id):
    """
    Создание записи в таблице Problem.
    """
    user = get_object_or_404(UserFromTelegram, telegram_id=telegram_id)
    serializer = ProblemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
