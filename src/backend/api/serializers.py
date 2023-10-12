from django.template.loader import render_to_string
from rest_framework import serializers

from api.models import (
    Answer,
    Problem,
    Question,
    ResultStatus,
    TaskStatus,
    UserFromTelegram,
)


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор получения вопроса задания."""

    class Meta:
        model = Question
        fields = ("content",)

    def to_representation(self, obj):
        return {"count": obj.count(), "result": self._get_result(obj)}

    def _get_result(self, obj: list[Question]):
        result = []
        task_number = self.context["task_number"]
        template_name = self._get_template_name_by_task_number(task_number)
        for question in obj:
            result.append(
                {
                    "content": render_to_string(
                        template_name,
                        {"question": question},
                        self.context["request"],
                    )
                }
            )
        return result

    @staticmethod
    def _get_template_name_by_task_number(task_number):
        if task_number == 3 or task_number == 8:
            template_name = "questions/question_with_pairs_format.html"
        else:
            template_name = "questions/standard_question_format.html"
        return template_name


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


class UserFromTelegramUpdateSerializer(UserFromTelegramRetrieveCreateSerializer):
    """
    Сериализатор модели `UserFromTelegram`.
    Используется для:
    - Изменения полей name и surname в объекте модели UserFromTelegram.
    """

    class Meta(UserFromTelegramRetrieveCreateSerializer.Meta):
        read_only_fields = ("telegram_id", "telegram_username")


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


class TaskResultsForUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели 'ResultStatus'.
    Используется для:
    - Получения результата выполнения конкретного задания
    конкретным пользователем.
    """

    title = serializers.ReadOnlyField(source="result.title")
    description = serializers.ReadOnlyField(source="result.description")

    class Meta:
        model = ResultStatus
        fields = ["title", "description"]

    def to_representation(self, obj):
        results = []
        task_number = self.context["task_number"]
        template_name = self._get_template_name_by_task_number(task_number)
        for result in obj:
            results.append(
                {
                    "content": render_to_string(
                        template_name,
                        {
                            "result": result.result,
                            "result_status": result,
                        },
                    )
                }
            )
        return {"count": len(results), "result": results}

    @staticmethod
    def _get_template_name_by_task_number(task_number):
        if task_number == 2:
            template_name = "results/result_with_you_and_dash_format.html"
        else:
            template_name = "results/standard_result_format.html"
        return template_name


class ProblemSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Problem.
    """

    message = serializers.CharField(required=True)

    class Meta:
        model = Problem
        fields = ("id", "user", "message", "answer", "create_date")
        read_only_fields = ("user", "answer")
