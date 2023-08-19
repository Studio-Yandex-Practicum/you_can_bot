from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import QuestionSerializer


@api_view(['POST'])
def create_question(request, telegram_id):
    data = {'telegram_id': telegram_id, 'message': request.data.get('message')}
    serializer = QuestionSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
