from django.conf import settings
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
        help_text='Введите номер задания'
    )
    answers = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='task_status',
        verbose_name='Ответы',
        help_text='Укажите ответы'
    )
    summary = models.TextField(
        'Расшифровка',
        help_text='Введите расшифровку'
    )
    is_done = models.BooleanField(
        'Статус выполнения',
        default=False
    )
    pass_date = models.DateTimeField(
        'Дата выполнения',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'статус'
        verbose_name_plural = '2. Статусы заданий'

    def __str__(self):
        return f'{self.number} {self.summary} {self.is_done} {self.pass_date}'


class Question(models.Model):
    """Модель вопросов."""

    message = models.TextField(
        'Содержание вопроса',
        help_text='Введите вопрос'
    )
    answer = models.TextField(
        'Варианты ответа',
        help_text='Введите варианты ответа'
    )
    create_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'вопрос'
        verbose_name_plural = '4. Вопросы'

    def __str__(self):
        return f'{self.message} {self.answer} {self.create_date}'


class UserFromTelegram(models.Model):
    """Модель пользователя в Телеграме."""

    telegram_id = models.IntegerField(
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
    tasks = models.ForeignKey(
        TaskStatus,
        on_delete=models.CASCADE,
        related_name='telegram_user',
        verbose_name='Пройденные задания'
    )
    questions = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='telegram_user',
        verbose_name='Ответы пользователя'
    )
    mentor = models.CharField(
        'Ментор',
        max_length=settings.MAX_LENGTH_SURNAME
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'пользователя'
        verbose_name_plural = '1. Пользователи из Телеграма'

    def __str__(self):
        return f'{self.telegram_id} {self.name} {self.surname}'
