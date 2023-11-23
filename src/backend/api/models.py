from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

_MAX_LENGTH_OF_TELEGRAM_USERNAME = 32

User = get_user_model()


class MentorProfile(models.Model):
    """Модель профиля психолога."""

    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, related_name="mentorprofile"
    )
    telegram_id = models.PositiveBigIntegerField(
        "Айди Telegram",
        help_text="На этот id в Telegram могут быть отправлены уведомления",
        unique=True,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Профиль психолога"
        verbose_name_plural = "Профили психологов"

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

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"
        ordering = ("number",)

    def __str__(self):
        return f"Задание {self.number}"


class Photo(models.Model):
    file_id = models.TextField(
        "ID для telegram",
        help_text=(
            "После загрузки в telegram файлу будет"
            " присвоен file_id для повторной отправки."
        ),
        default="",
        blank=True,
    )
    image = models.ImageField(
        "Картинка",
        upload_to="questions/",
    )

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"


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
    content = models.TextField("Текст вопроса")
    example = models.TextField(
        "Пример ответа",
        default="",
        blank=True,
    )
    photo = models.OneToOneField(
        verbose_name="Картинка",
        to=Photo,
        on_delete=models.SET_NULL,
        related_name="question",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        constraints = [
            models.UniqueConstraint(
                fields=("task", "number"), name="unique_task_question_number"
            ),
        ]
        ordering = ("number",)

    def __str__(self):
        return self.content


class Choice(models.Model):
    question = models.ForeignKey(
        verbose_name="Вопрос",
        to=Question,
        on_delete=models.CASCADE,
        related_name="choices",
    )
    title = models.TextField("Заголовок")
    description = models.TextField(
        "Описание",
        default="",
        blank=True,
    )

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        return self.title


class Result(models.Model):
    task = models.ForeignKey(
        verbose_name="Задание",
        to=Task,
        on_delete=models.CASCADE,
        related_name="results",
    )
    key = models.TextField(
        "Ключ",
        help_text=(
            "Значение, полученное в ходе расшифровки, которое используется"
            " как краткая запись результата. Например, ISTP."
        ),
    )
    title = models.TextField("Заголовок")
    description = models.TextField(
        "Описание",
        default="",
        blank=True,
    )

    class Meta:
        verbose_name = "результат"
        verbose_name_plural = "Результаты заданий"
        unique_together = ("task", "key")

    def __str__(self):
        return self.title


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
    is_done = models.BooleanField(
        "Выполнено",
        default=False,
        help_text="Чтобы сбросить выполнение задания и дать подростку пройти его"
        " заново, уберите здесь галочку. Также выставите в поле"
        " 'Текущий вопрос' значение 0.",
    )
    pass_date = models.DateTimeField(
        "Дата выполнения",
        null=True,
        blank=True,
        default=None,
        db_index=True,
    )
    current_question = models.PositiveSmallIntegerField(
        "Текущий номер вопроса",
        default=0,
    )

    class Meta:
        ordering = ("pk",)
        verbose_name = "статус"
        verbose_name_plural = "Статусы заданий"
        unique_together = ("user", "task")

    def __str__(self):
        return f"Сводка пользователя {self.user}. {self.task}"


class Answer(models.Model):
    """Модель ответов на вопросы."""

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
        related_name="answers",
    )
    content = models.TextField("Ответ")

    class Meta:
        ordering = ("pk",)
        verbose_name = "ответ"
        verbose_name_plural = "Ответы на задания"

    def __str__(self):
        return f"На вопрос {self.question.number}"


class ResultStatus(models.Model):
    task_status = models.ForeignKey(
        verbose_name="Сводка",
        to=TaskStatus,
        on_delete=models.CASCADE,
        related_name="result",
    )
    top = models.PositiveSmallIntegerField(
        "Место в топе",
        validators=(MinValueValidator(limit_value=1),),
        default=1,
    )
    result = models.ForeignKey(
        verbose_name="Результат",
        to=Result,
        on_delete=models.PROTECT,
    )
    score = models.PositiveSmallIntegerField(
        "Баллы",
        default=0,
    )

    class Meta:
        verbose_name = "Результат пользователя"
        verbose_name_plural = "Результаты пользователя"
        ordering = ("top",)

    def __str__(self):
        return f"{self.result} ({self.score} б.)"


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
        blank=True,
    )
    create_date = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ("-pk",)
        verbose_name = "вопрос"
        verbose_name_plural = "Вопросы от пользователей"

    def __str__(self):
        return self.message
