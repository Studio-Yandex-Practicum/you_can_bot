from rest_framework import serializers

from .models import TaskStatus


class TaskStatusListSerializer(serializers.ModelSerializer):
    """
    Сериализватор модели 'TaskStatus'.
    Используется для получения списка заданий по telegram_id
    """

    class Meta:
        model = TaskStatus
        fields = ["number", "is_done"]


class TaskStatusRetriveSerializer(serializers.ModelSerializer):
    """
    Сериализватор модели 'TaskStatus'.
    Используется для:
    - Получения информации о статусе выполнения конкретного задания
    """

    class Meta:
        model = TaskStatus
        fields = ["number", "current_question", "summary", "is_done"]
