import asyncio
import html
import logging

from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.html import format_html
from telegram.error import (
    BadRequest,
    Forbidden,
    NetworkError,
    RetryAfter,
    TelegramError,
)
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

logger = logging.getLogger(__name__)
User = get_user_model()

PROBLEM_ANSWER = (
    "Профдизайнер ответил на ваш вопрос: «{question}».\n\n<b>Ответ:</b> «{content}»"
)
ANSWER_HELP_TEXT = (
    "Сообщение пользователю рендерится с HTML-разметкой Telegram. "
    "Поддерживаются теги &lt;b&gt;, &lt;i&gt;, &lt;a href=&quot;...&quot;&gt;, "
    "&lt;code&gt;, &lt;pre&gt;. "
    "Знаки «&lt;», «&gt;» и «&amp;» в обычном тексте экранируйте как "
    "&amp;lt;, &amp;gt;, &amp;amp;, иначе Telegram отклонит сообщение."
)
SEND_ERROR_BAD_REQUEST = (
    "Telegram отверг сообщение — скорее всего, в ответе есть неэкранированные "
    "символы «<», «>», «&» или неподдерживаемый HTML-тег. Ответ не сохранён."
)
SEND_ERROR_FORBIDDEN = (
    "Пользователь заблокировал бота, доставить ответ невозможно. " "Ответ не сохранён."
)
SEND_ERROR_NETWORK = (
    "Не удалось доставить ответ пользователю в Telegram (сетевая ошибка). "
    "Ответ не сохранён, попробуйте ещё раз через минуту."
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


class ProblemForm(forms.ModelForm):
    """Форма Problem: отправляет ответ в Telegram до сохранения в БД."""

    class Meta:
        model = Problem
        fields = "__all__"
        help_texts = {"answer": ANSWER_HELP_TEXT}

    def clean(self):
        cleaned = super().clean()
        if self._should_notify(cleaned):
            self._notify_user(cleaned["answer"])
        return cleaned

    def _should_notify(self, cleaned):
        return bool(
            self.instance.pk and "answer" in self.changed_data and cleaned.get("answer")
        )

    def _notify_user(self, answer):
        try:
            asyncio.run(
                non_context_send_message(
                    text=PROBLEM_ANSWER.format(
                        question=html.escape(self.instance.message),
                        content=answer,
                    ),
                    user_id=self.instance.user.telegram_id,
                    parse_mode="HTML",
                )
            )
        except BadRequest as error:
            logger.warning(
                "Telegram BadRequest при отправке ответа problem %s: %s",
                self.instance.pk,
                error,
            )
            raise ValidationError({"answer": SEND_ERROR_BAD_REQUEST})
        except Forbidden as error:
            logger.info(
                "Пользователь %s заблокировал бота, ответ problem %s не доставлен: %s",
                self.instance.user.telegram_id,
                self.instance.pk,
                error,
            )
            raise ValidationError({"answer": SEND_ERROR_FORBIDDEN})
        except (RetryAfter, NetworkError, TelegramError) as error:
            logger.warning(
                "Не удалось доставить ответ problem %s: %s",
                self.instance.pk,
                error,
            )
            raise ValidationError({"answer": SEND_ERROR_NETWORK})


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    form = ProblemForm
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
