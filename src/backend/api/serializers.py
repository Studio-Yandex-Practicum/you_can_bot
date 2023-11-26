from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
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
from api.utils import create_available_username

User = get_user_model()


MENTOR_CREATE_ERROR = "Учетная запись с указанным telegram_id уже существует."


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
            content = render_to_string(
                template_name,
                {"question": question},
                self.context["request"],
            )
            photo = question.photo
            if photo and photo.image:
                photo_url = urljoin(f"http://{settings.DOMAIN}", photo.image.url)
                content = f"<a href='{photo_url}'>&#8205;</a>" + content
            result.append({"content": content})
        return result

    @staticmethod
    def _get_template_name_by_task_number(task_number):
        if task_number == 3 or task_number == 8:
            template_name = "questions/question_with_pairs_format.html"
        elif 5 <= task_number <= 7:
            template_name = "questions/simple_question_format.html"
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

    def to_representation(self, obj):
        if self.context.get("as_result"):
            results = []
            task_number = self.context["task_number"]
            template_name = self._get_template_name_by_task_number(task_number)
            for answer in obj:
                results.append(
                    {"content": render_to_string(template_name, {"answer": answer})}
                )
            return {"count": len(results), "result": results}
        return super().to_representation(obj)

    @staticmethod
    def _get_template_name_by_task_number(task_number):
        if task_number == 6:
            template_name = "results/result_with_answer_numeric.html"
        elif task_number == 7:
            template_name = "results/result_with_answer_line_break.html"
        else:
            template_name = "results/result_with_answer.html"
        return template_name


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


class MentorSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели 'User'.
    Используется для:
    - Создания учетной записи психолога.
    """

    telegram_id = serializers.IntegerField(source="mentorprofile.telegram_id")
    username = serializers.ReadOnlyField()
    password = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "telegram_id",
            "username",
            "password",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate_telegram_id(self, value):
        """
        Проверяет отсутствие учетной записи психолога с указанным telegram_id.
        """
        if User.objects.filter(mentorprofile__telegram_id=value).exists():
            raise serializers.ValidationError(detail=MENTOR_CREATE_ERROR)
        return value

    def validate(self, attrs):
        """
        Добавляет случайно сгенерированный пароль в словарь validated_data.
        """
        attrs["password"] = User.objects.make_random_password()
        return attrs

    def get_password(self, obj):
        return self.validated_data.get("password")

    def create(self, validated_data):
        """
        Создает учетную запись психолога и добавляет ее в группу Mentor.
        """
        profile = validated_data.get("mentorprofile")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        password = validated_data.get("password")
        username = create_available_username(first_name=first_name, last_name=last_name)
        mentor = User(username=username, first_name=first_name, last_name=last_name)
        mentor.set_password(password)
        mentor._telegram_id = profile.get("telegram_id")
        mentor.save()
        mentor_group = Group.objects.get(name="Mentor")
        mentor.groups.add(mentor_group)
        return mentor
