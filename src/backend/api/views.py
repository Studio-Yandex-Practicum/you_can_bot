
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Answer, UserFromTelegram, TaskStatus
from .serializers import AnswerSerializer
from django.shortcuts import get_object_or_404


@api_view(('POST',))
def answer_create(request, telegram_id, task_number):
    """Занесение ответа от пользователя в Answer."""
    user = get_object_or_404(UserFromTelegram, telegram_id=telegram_id)
    task = get_object_or_404(TaskStatus, user=user)
    serializer = AnswerSerializer(data=request.data, context={'task': task.pk})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)



# POST http://127.0.0.1:8000/api/v1/users/12345/tasks/1/answers/
# Content-Type: application/json

# {
#     "number": "1",
#     "content": "a"
# }

# Примечание: должно также изменяться current_question объекта TaskStatus,
# на который ссылается атрибут task объекта Answer
