from rest_framework import serializers

from api.models import Answer, TaskStatus, UserFromTelegram


class AnswerSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Answer.
    """

    number = serializers.IntegerField(source="question.number", read_only=True)

    class Meta:
        model = Answer
        fields = ("id", "number", "content")


class UserFromTelegramRetrieveCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели `UserFromTelegram`.
    Используется для:
    - Получения информации по telegram_id (GET);
    - Создания новой записи в модель `UserFromTelegram` (POST).
    """

    class Meta:
        model = UserFromTelegram
        fields = ("telegram_id", "telegram_username", "name", "surname")
        extra_kwargs = {"telegram_username": {"write_only": True}}


class UserFromTelegramUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели `UserFromTelegram`.
    Используется для:
    - Изменения полей name и surname в объекте модели UserFromTelegram.
    """

    class Meta:
        model = UserFromTelegram
        fields = ("telegram_id", "name", "surname")
        read_only_fields = ("telegram_id",)


class TaskStatusSerializer(serializers.ModelSerializer):
    """
    Сериализватор модели 'TaskStatus'.
    Используется для получения списка заданий по telegram_id
    """

    number = serializers.IntegerField(source="task.number", read_only=True)

    class Meta:
        model = TaskStatus
        fields = ["number", "is_done"]


class TaskStatusRetrieveSerializer(TaskStatusSerializer):
    """
    Сериализватор модели 'TaskStatus'.
    Используется для:
    - Получения информации о статусе выполнения конкретного задания
    """

    class Meta:
        model = TaskStatus
        fields = ["number", "current_question", "is_done"]
