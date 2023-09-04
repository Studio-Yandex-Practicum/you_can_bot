from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

_MAX_LENGTH_OF_TELEGRAM_USERNAME = 32

User = get_user_model()


class MentorProfile(models.Model):
    """Модель профиля психолога."""

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
    )
    telegram_username = models.CharField(
        "Никнейм Telegram",
        help_text="На этот никнейм в Telegram могут быть отправлены уведомления",
        max_length=_MAX_LENGTH_OF_TELEGRAM_USERNAME,
        unique=True,
    )

    class Meta:
        verbose_name = "Профиль"

    def __str__(self):
        return f"{self.user}"


class UserFromTelegram(models.Model):
    """Модель пользователя из Telegram."""

    telegram_id = models.PositiveBigIntegerField(
        "Telegram ID",
        unique=True,
    )
    telegram_username = models.CharField(
        "Никнейм Telegram",
        max_length=_MAX_LENGTH_OF_TELEGRAM_USERNAME,
    )
    name = models.CharField(
        "Имя",
        max_length=settings.MAX_LENGTH_NAME,
    )
    surname = models.CharField(
        "Фамилия",
        max_length=settings.MAX_LENGTH_SURNAME,
    )
    mentor = models.ForeignKey(
        verbose_name="Психолог",
        to=MentorProfile,
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        ordering = ("pk",)
        verbose_name = "пользователя"
        verbose_name_plural = "Пользователи из Telegram"

    def __str__(self):
        return f"{self.name} {self.surname}"


class Task(models.Model):
    class TaskNumber(models.IntegerChoices):
        FIRST = 1, "Задание 1"
        SECOND = 2, "Задание 2"
        THIRD = 3, "Задание 3"
        FOURTH = 4, "Задание 4"
        FIFTH = 5, "Задание 5"
        SIXTH = 6, "Задание 6"
        SEVENTH = 7, "Задание 7"
        EIGHTH = 8, "Задание 8"

    number = models.PositiveSmallIntegerField(
        "Номер задания",
        choices=TaskNumber.choices,
        primary_key=True,
    )
    end_question = models.PositiveSmallIntegerField(
        "Последний номер задания",
    )

    def __str__(self):
        return f"Задание {self.number}"


class Question(models.Model):
    task = models.ForeignKey(
        verbose_name="Задание",
        to=Task,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    number = models.PositiveSmallIntegerField(
        "Номер вопроса",
        validators=(MinValueValidator(limit_value=1),),
    )
    content = models.TextField()
    example = models.TextField(default="")

    def __str__(self):
        return str(self.number)


class Choice(models.Model):
    question = models.ForeignKey(
        verbose_name="Вопрос",
        to=Question,
        on_delete=models.CASCADE,
        related_name="choices",
    )
    title = models.TextField()
    description = models.TextField(default="")


class TaskStatus(models.Model):
    """Модель статуса выполнения задания пользователем."""

    user = models.ForeignKey(
        verbose_name="Пользователь",
        to=UserFromTelegram,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    task = models.ForeignKey(
        verbose_name="Задание",
        to=Task,
        on_delete=models.PROTECT,
    )
    summary = models.TextField(
        "Расшифровка",
        default="",
    )
    is_done = models.BooleanField(
        "Выполнено",
        default=False,
    )
    pass_date = models.DateTimeField(
        "Дата выполнения",
        null=True,
        default=None,
        db_index=True,
    )
    current_question = models.PositiveSmallIntegerField(
        "Текущий номер задания",
        default=0,
    )

    class Meta:
        ordering = ("pk",)
        verbose_name = "статус"
        verbose_name_plural = "Статусы заданий"
        unique_together = ("user", "task")


class Answer(models.Model):
    """Модель ответов на вопросы заданий."""

    task_status = models.ForeignKey(
        verbose_name="Задание",
        to=TaskStatus,
        on_delete=models.CASCADE,
        related_name="answers",
    )
    question = models.ForeignKey(
        verbose_name="Вопрос",
        to=Question,
        on_delete=models.PROTECT,
    )
    content = models.TextField("Ответ")

    class Meta:
        ordering = ("pk",)
        verbose_name = "ответ"
        verbose_name_plural = "Ответы на задания"

    def __str__(self):
        return f"Ответ {self.question}"


class Problem(models.Model):
    """Модель вопросов от пользователей телеграм."""

    user = models.ForeignKey(
        verbose_name="Пользователь",
        to=UserFromTelegram,
        on_delete=models.CASCADE,
        related_name="problems",
    )
    message = models.TextField(
        "Вопрос",
    )
    answer = models.TextField(
        "Ответ психолога",
        default="",
    )
    create_date = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ("pk",)
        verbose_name = "вопрос"
        verbose_name_plural = "Вопросы от пользователей"

    def __str__(self):
        return self.message
