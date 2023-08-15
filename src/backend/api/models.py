from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.core.validators import MaxValueValidator, MinValueValidator
# https://lucid.app/lucidchart/51f93cb7-9379-4588-be1b-61ddf4d9d637/view?page=0_0#


class TaskStatus(models.Model):
    """Модель Заданий."""

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
        verbose_name = 'тег'
        verbose_name_plural = '2. Статусы заданий'

    def __str__(self):
        return f'{self.number} {self.summary} {self.is_done} {self.pass_date}'


# class Recipe(models.Model):
#     """Модель рецептов."""

#     pub_date = models.DateTimeField(
#         'Дата создания',
#         auto_now_add=True,
#         db_index=True
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='recipes',
#         verbose_name='Автор',
#         help_text='Укажите автора рецепта'
#     )
#     ingredients = models.ManyToManyField(
#         Ingredient,
#         through='RecipeIngredient',
#         related_name='recipes',
#         verbose_name='Ингридиенты',
#         help_text='Введите используемые ингридиенты'
#     )
    
#     name = models.CharField(
#         'Наименование рецепта',
#         max_length=settings.MAX_LENGTH_RECIPE_NAME,
#         help_text='Введите наименование рецепта'
#     )
#     text = models.TextField(
#         'Описание',
#         help_text='Введите описание рецепта'
#     )
#     cooking_time = models.PositiveIntegerField(
#         validators=[
#             MinValueValidator(
#                 settings.MIN_COOKING_TIME, settings.COOKING_TIME_MESSAGE
#             ),
#             MaxValueValidator(
#                 settings.MAX_COOKING_TIME, settings.COOKING_TIME_MESSAGE
#             )
#         ],
#         verbose_name='Время приготовления',
#         help_text='Введите время приготовления (в минутах)'
#     )

#     class Meta:
#         ordering = ('pub_date',)
#         verbose_name = 'рецепт'
#         verbose_name_plural = '3. Рецепты'

#     def __str__(self):
#         return self.name


class User(AbstractUser):
    """Кастомная модель пользователя."""

    telegram_id = models.IntegerField(
        'Telegram ID',
        max_length=settings.MAX_LENGTH_EMAIL,
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
        related_name='user',
        verbose_name='Пользователь'
    )
    questions = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь'
    )
    mentor = models.CharField(
        'Ментор',
        max_length=settings.MAX_LENGTH_SURNAME
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'пользователя'
        verbose_name_plural = '1. Пользователи'
        # constraints = [
        #     models.CheckConstraint(
        #         check=~models.Q(user=models.F('author')),
        #         name='user is not author',
        #     ),
        #     models.UniqueConstraint(
        #         fields=['user', 'author'], name='unique_following')
        # ]
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['user', 'recipe'], name='unique_shopping_cart')
        # ]

    def __str__(self):
        return f'{self.telegram_id} {self.name} {self.surname}'
