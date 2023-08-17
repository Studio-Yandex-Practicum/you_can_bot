from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Answer(models.Model):
    """Модель ответов."""

    number = models.PositiveIntegerField(
        'Номер ответа',
        help_text='Введите номер ответа'
    )
    content = models.CharField(
        'Содержание ответа',
        help_text='Введите содержание ответа',
        max_length=settings.MAX_LENGTH_COMMON_CHARFIELD
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'ответ'
        verbose_name_plural = '3. Ответы на задания'

    def __str__(self):
        return f'{self.number} {self.content}'


class TaskStatus(models.Model):
    """Модель заданий."""

    number = models.PositiveIntegerField(
        'Номер задания',
        help_text='Введите номер задания',
        validators=[
            MinValueValidator(
                settings.MIN_TASK_NUMBER,
                settings.TASK_NUMBER_MESSAGE
            ),
            MaxValueValidator(
                settings.MAX_TASK_NUMBER,
                settings.TASK_NUMBER_MESSAGE
            )
        ],
    )
    answers = models.ManyToManyField(
        Answer,
        through='TaskStatusAnswer',
        related_name='task_status',
        verbose_name='Ответы пользователя',
        help_text='Введите ответы'
    )
    summary = models.TextField(
        'Расшифровка',
        help_text='Введите расшифровку',
        blank=True
    )
    is_done = models.BooleanField(
        'Статус выполнения',
        default=False
    )
    pass_date = models.DateTimeField(
        'Дата выполнения',
        default=None,
        db_index=True
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'статус'
        verbose_name_plural = '2. Статусы заданий'

    def __str__(self):
        return f'{self.number} {self.summary} {self.is_done} {self.pass_date}'


class TaskStatusAnswer(models.Model):
    """
    У задания может быть несколько попыток прохождения.
    В этой модели будут связаны:
    1) id заданий
    2) id пула ответов.
    """

    task_status = models.ForeignKey(
        TaskStatus,
        on_delete=models.CASCADE,
        verbose_name='Номер задания',
        help_text='Введите номер задания'
    )
    answers = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        verbose_name='Номер пула ответов',
        help_text='Введите ID пула ответов'
    )
    
    class Meta:
        ordering = ('pk',)
        verbose_name = 'номер задания'

    def __str__(self):
        return f'{self.task_status.pk} {self.answers.pk}'


class Problem(models.Model):
    """Модель вопросов от пользователей телеграм."""

    message = models.TextField(
        'Содержание вопроса',
        help_text='Введите вопрос'
    )
    answer = models.TextField(
        'Ответ психолога',
        help_text='Введите ответ психолога',
        blank=True
    )
    # Может есть смысл добавить дату создания?
    # create_date = models.DateTimeField(
    #     'Дата создания',
    #     auto_now_add=True,
    #     db_index=True
    # )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'вопрос'
        verbose_name_plural = '4. Вопросы от пользователей'

    def __str__(self):
        return f'{self.message} {self.answer}'


class UserFromTelegram(models.Model):
    """Модель пользователя в Телеграме."""
    
    # Плохая идея исплользовать telegram_id в качестве pk.
    # Для базы лучше, чтобы pk постепенно (инкрементально) увеличивался.
    # Это избавит от проблем в дальнейшей при работе непосредственно с СУБД.
    telegram_id = models.PositiveBigIntegerField(
        'Telegram ID',
        unique=True
    )
    name = models.CharField(
        'Имя',
        max_length=settings.MAX_LENGTH_NAME
    )
    surname = models.CharField(
        'Фамилия',
        max_length=settings.MAX_LENGTH_SURNAME
    )
    tasks = models.ManyToManyField(
        TaskStatus,
        through='UserFromTelegramTaskStatus',
        related_name='telegram_user',
        verbose_name='Задания, решенные пользователем',
        help_text='Введите задания'
    )
    problems = models.ManyToManyField(
        Problem,
        through='UserFromTelegramProblem',
        related_name='telegram_user',
        verbose_name='Вопросы от пользователя',
        help_text='Введите вопросы от пользователя'
    )
    mentor = models.CharField(
        'Психолог',
        max_length=settings.MAX_LENGTH_SURNAME,
        blank=True
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'пользователя'
        verbose_name_plural = '1. Пользователи из Телеграма'

    def __str__(self):
        return f'{self.telegram_id} {self.name} {self.surname}'


class UserFromTelegramProblem(models.Model):
    """
    У одного пользователя может быть несколько проблемных вопросов.
    В этой модели будут связаны:
    1) id пользователей из Телеграм
    2) id проблемных вопросов.
    """

    user = models.ForeignKey(
        UserFromTelegram,
        on_delete=models.CASCADE,
        verbose_name='Пользователь из Телеграма',
        help_text='Введите ID пользователя'
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        verbose_name='Проблемный вопрос',
        help_text='Введите ID проблемного вопроса'
    )
    
    class Meta:
        ordering = ('pk',)
        verbose_name = 'пользователь, добавивший проблемный вопрос'

    def __str__(self):
        return f'{self.user.name} {self.problem.message}'


class UserFromTelegramTaskStatus(models.Model):
    """
    У одного пользователя может быть несколько решенных заданий.
    В этой модели будут связаны:
    1) id пользователей из Телеграм
    2) id решенных заданий.
    """

    user = models.ForeignKey(
        UserFromTelegram,
        on_delete=models.CASCADE,
        verbose_name='Пользователь из Телеграма',
        help_text='Введите ID пользователя'
    )
    task = models.ForeignKey(
        TaskStatus,
        on_delete=models.CASCADE,
        verbose_name='Решенное задание',
        help_text='Введите ID решенного задания'
    )
    
    class Meta:
        ordering = ('pk',)
        verbose_name = 'Пользователь, решивший задание'

    def __str__(self):
        return f'{self.user.name} {self.task.number}'
