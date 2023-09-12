from django.template.loader import render_to_string
from rest_framework import serializers

from api.models import (Answer, Question, TaskStatus,
                        UserFromTelegram, ResultStatus)


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор получения вопроса задания."""

    class Meta:
        model = Question
        fields = ("content",)

    def to_representation(self, obj):
        return {"count": obj.count(), "result": self._get_result(obj)}

    def _get_result(self, obj):
        result = []
        for question in obj:
            result.append(
                {
                    "content": render_to_string(
                        "questions/standard_question_format.html",
                        {"question": question},
                        self.context["request"],
                    )
                }
            )
        return result


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
        fields = ["number", "current_question", "summary", "is_done"]


class TaskResultsForUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели 'ResultStatus'.
    Используется для:
    - Получения результата выполнения конкретного задания
    конкретным пользователем.
    """

    title = serializers.ReadOnlyField(source='result.title')
    description = serializers.ReadOnlyField(source='result.description')

    class Meta:
        model = ResultStatus
        fields = ['title', 'description']

    def to_representation(self, obj):
        results = []
        for result in obj:
            results.append(
                {
                    'content':
                        render_to_string(
                            "results/results_for_user_by_task.html",
                            {'result': result.result}
                        )
                }
            )
        return {
            "count": len(results),
            "result": results
        }
