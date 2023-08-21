from rest_framework import serializers

from .models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Answer.
    """

    class Meta:
        model = Answer
        fields = '__all__'
