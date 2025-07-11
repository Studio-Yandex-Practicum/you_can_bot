import asyncio

from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from tinymce.widgets import TinyMCE

from api.models import (
    Answer,
    Choice,
    MentorProfile,
    Photo,
    Problem,
    Question,
    Result,
    ResultStatus,
    Task,
    TaskStatus,
    UserFromTelegram,
)

from .conversation_utils import non_context_send_message
from .filters import ANSWER_NOT_RECEIVED, ANSWER_RECEIVED, ProblemAnswerFilter

User = get_user_model()

PROBLEM_ANSWER = (
    "Профдизайнер ответил на ваш вопрос: «{question}».\n\n<b>Ответ:</b> «{content}»"
)


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0
    can_delete = False


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    show_change_link = True
    can_delete = False


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    can_delete = False


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        widgets = {"key": forms.TextInput}
        fields = "__all__"


class ResultsInline(admin.StackedInline):
    model = Result
    extra = 0
    can_delete = False
    form = ResultForm


class ResultStatusInline(admin.StackedInline):
    model = ResultStatus
    extra = 0
    can_delete = False


class TaskStatusInline(admin.TabularInline):
    model = TaskStatus
    extra = 0
    show_change_link = True
    can_delete = False
    readonly_fields = ["user", "task", "pass_date", "is_done", "current_question"]


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "message",
        "answer",
        "create_date",
        "get_answer_status",
    )
    list_display_links = ("message",)
    search_fields = (
        "user__name",
        "user__surname",
        "user__telegram_username",
    )
    date_hierarchy = "create_date"
    empty_value_display = "-пусто-"
    list_filter = (ProblemAnswerFilter,)

    def save_model(self, request, obj, form, change):
        if change and "answer" in form.changed_data:
            asyncio.run(
                non_context_send_message(
                    text=PROBLEM_ANSWER.format(
                        question=obj.message, content=obj.answer
                    ),
                    user_id=obj.user.telegram_id,
                )
            )
        super().save_model(request, obj, form, change)

    @admin.display(description="Статус ответа")
    def get_answer_status(self, obj):
        if obj.answer:
            return ANSWER_RECEIVED
        return ANSWER_NOT_RECEIVED


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "end_question",
    )
    inlines = (QuestionInline, ResultsInline)


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "user",
        "current_question",
        "is_done",
        "pass_date",
    )
    search_fields = (
        "user__name",
        "user__surname",
        "user__telegram_username",
    )
    inlines = (AnswerInline, ResultStatusInline)
    list_filter = (
        "task",
        "is_done",
    )
    date_hierarchy = "pass_date"
    readonly_fields = ["user", "task", "pass_date"]


class UserFromTelegramForm(forms.ModelForm):
    class Meta:
        model = UserFromTelegram
        widgets = {"test_summary": TinyMCE(attrs={"cols": 80, "rows": 30})}
        fields = "__all__"


@admin.register(UserFromTelegram)
class UserFromTelegramAdmin(admin.ModelAdmin):
    form = UserFromTelegramForm
    date_hierarchy = "last_task_completed_at"
    list_display = (
        "telegram_username",
        "name",
        "surname",
        "mentor",
        "tasks_completed_count",
        "last_task_completed_at",
        "info_page",
    )
    search_fields = (
        "name",
        "surname",
        "telegram_username",
    )
    list_filter = (
        "mentor",
        "tasks_completed_count",
    )
    empty_value_display = "-пусто-"
    inlines = (TaskStatusInline,)

    @admin.display(description="Общая сводка")
    def info_page(self, obj):
        user_url = reverse(
            "info_pages:taskstatus-list", kwargs=dict(telegram_id=obj.telegram_id)
        )
        return format_html('<a href="{url}">Перейти</a>', url=user_url)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "content",
    )
    list_display_links = (
        "number",
        "content",
    )
    list_filter = ("task",)
    inlines = (ChoiceInline,)


class MentorProfileInline(admin.StackedInline):
    model = MentorProfile
    can_delete = False


class ExtendedUserAdmin(UserAdmin):
    inlines = (MentorProfileInline,)


admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
admin.site.register(Photo)
