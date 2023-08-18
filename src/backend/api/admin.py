from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from api.models import Answer, MentorProfile, Problem, TaskStatus, UserFromTelegram

User = get_user_model()


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0


class ProblemInline(admin.StackedInline):
    model = Problem
    extra = 0


class TaskStatusInline(admin.TabularInline):
    model = TaskStatus
    extra = 0
    show_change_link = True


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "message",
        "answer",
        "create_date",
    )
    list_display_links = ("message",)
    search_fields = (
        "user__name",
        "user__surname",
        "user__telegram_username",
    )
    date_hierarchy = "create_date"
    empty_value_display = "-пусто-"


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "content",
        "task",
        "user",
    )
    list_display_links = (
        "number",
        "content",
    )
    search_fields = (
        "task__user__name",
        "task__user__surname",
        "task__user__telegram_username",
    )
    list_filter = (
        "number",
        "task__number",
    )
    empty_value_display = "-пусто-"

    @staticmethod
    def user(obj):
        return obj.task.user


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "summary",
        "user",
        "current_question",
        "end_question",
        "is_done",
        "pass_date",
    )
    search_fields = (
        "user__name",
        "user__surname",
        "user__telegram_username",
    )
    inlines = (AnswerInline,)
    list_filter = (
        "number",
        "is_done",
    )
    date_hierarchy = "pass_date"


@admin.register(UserFromTelegram)
class UserFromTelegramAdmin(admin.ModelAdmin):
    list_display = (
        "telegram_username",
        "name",
        "surname",
        "mentor",
    )
    search_fields = (
        "name",
        "surname",
        "telegram_username",
    )
    list_filter = ("mentor",)
    empty_value_display = "-пусто-"
    inlines = (ProblemInline, TaskStatusInline)


class MentorProfileInline(admin.StackedInline):
    model = MentorProfile
    can_delete = False


class ExtendedUserAdmin(UserAdmin):
    inlines = (MentorProfileInline,)


admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
