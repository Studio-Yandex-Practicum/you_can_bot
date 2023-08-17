from django.contrib import admin

from api.models import (
    Answer, TaskStatus, TaskStatusAnswer, Problem, UserFromTelegram,
    UserFromTelegramProblem, UserFromTelegramTaskStatus
)


class ProblemInline(admin.TabularInline):
    """
    Вспомогательная модель для работы inlines.
    Обеспечивает функционал, чтобы проблемный вопрос,
    не привязанный к пользователю, нельзя было создать через админку.
    """

    model = UserFromTelegramProblem
    min_num = 1
    max_num = 1


class AnswerInline(admin.TabularInline):
    """
    Обеспечивает функционал, чтобы пул ответов,
    не привязанный к заданию, нельзя было создать через админку.
    """

    model = TaskStatusAnswer
    min_num = 1
    max_num = 1


class TaskStatusInline(admin.TabularInline):
    """
    Обеспечивает функционал, чтобы прохождение заданий,
    не привязанных к пользователю, нельзя было создать через админку.
    """

    model = UserFromTelegramTaskStatus
    min_num = 1
    max_num = 1


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'message',
        'answer'
    )
    list_editable = ('message', 'answer')
    search_fields = ('message', 'answer')
    empty_value_display = '-пусто-'
    inlines = [ProblemInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'number',
        'content'
    )
    list_editable = ('number', 'content')
    search_fields = ('number', 'content')
    empty_value_display = '-пусто-'
    inlines = [AnswerInline]


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'number',
        'summary',
        'is_done',
        'pass_date'
    )
    list_editable = ('number', 'summary', 'is_done')
    search_fields = ('number', 'summary', 'is_done', 'pass_date')
    inlines = [TaskStatusInline]


@admin.register(UserFromTelegram)
class UserFromTelegramAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'telegram_id',
        'name',
        'surname',
        'mentor'
    )
    list_editable = ('telegram_id', 'name', 'surname', 'mentor')
    search_fields = ('telegram_id', 'name', 'surname', 'mentor')
    empty_value_display = '-пусто-'
