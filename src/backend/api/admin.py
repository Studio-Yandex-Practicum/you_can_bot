from django.contrib import admin

from api.models import Answer, TaskStatus, Question, UserFromTelegram


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


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'number',
        'answers',
        'summary',
        'is_done',
        'pass_date'
    )
    list_editable = ('number', 'answers', 'summary', 'is_done')
    search_fields = ('number', 'answers', 'summary', 'is_done', 'pass_date')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'message',
        'answer',
        'create_date'
    )
    list_editable = ('message', 'answer')
    search_fields = ('message', 'answer', 'create_date')
    empty_value_display = '-пусто-'


@admin.register(UserFromTelegram)
class UserFromTelegramAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'telegram_id',
        'name',
        'surname',
        'tasks',
        'questions',
        'mentor'
    )
    list_editable = (
        'telegram_id', 'name', 'surname', 'tasks', 'questions', 'mentor'
    )
    search_fields = (
        'telegram_id', 'name', 'surname', 'tasks', 'questions', 'mentor'
    )
    empty_value_display = '-пусто-'
