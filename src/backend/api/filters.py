from django.contrib.admin import SimpleListFilter
from django.db.models import Q

from .models import Problem

ANSWER_RECEIVED = "Ответ получен"
ANSWER_NOT_RECEIVED = "Ответ не получен"


class AnswerFilter(SimpleListFilter):
    title = "Операция"  # or use _('country') for translated title
    parameter_name = "operation"

    def lookups(self, request, model_admin):
        return [
            (ANSWER_RECEIVED, ANSWER_RECEIVED),
            (ANSWER_NOT_RECEIVED, ANSWER_NOT_RECEIVED),
        ]

    def queryset(self, request, queryset):
        if self.value() == ANSWER_RECEIVED:
            return Problem.objects.filter(~~Q(answer=None))
        if self.value() == ANSWER_NOT_RECEIVED:
            return Problem.objects.filter(~Q(answer=None))
