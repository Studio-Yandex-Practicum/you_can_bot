from django.contrib.admin import SimpleListFilter
from django.db.models import Q

from .models import Problem

ANSWER_RECEIVED = "Ответ получен"
ANSWER_NOT_RECEIVED = "Ответ не получен"


class ProblemAnswerFilter(SimpleListFilter):
    title = "Наличие ответа"
    parameter_name = "answer_is_empty"

    def lookups(self, request, model_admin):
        return [
            ("true", ANSWER_NOT_RECEIVED),
            ("false", ANSWER_RECEIVED),
        ]

    def queryset(self, request, queryset):
        answer_is_empty = Q(answer="")
        if self.value() == "true":
            return Problem.objects.filter(answer_is_empty)
        if self.value() == "false":
            return Problem.objects.filter(~answer_is_empty)
