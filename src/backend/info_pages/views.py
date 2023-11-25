from django.db.models import Prefetch
from django.views.generic import DetailView

from api.mixins import IsStaffMixin
from api.models import Answer, ResultStatus, UserFromTelegram


class UserDetailView(IsStaffMixin, DetailView):
    queryset = UserFromTelegram.objects.select_related("mentor__user")
    slug_field = "telegram_id"
    slug_url_kwarg = "telegram_id"
    template_name = "info_pages/user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        task_statuses = (
            self.object.tasks.select_related("task")
            .prefetch_related(
                Prefetch(
                    "result",
                    queryset=ResultStatus.objects.select_related("result"),
                ),
                Prefetch(
                    "answers",
                    queryset=Answer.objects.select_related("question").prefetch_related(
                        "question__choices",
                    ),
                ),
            )
            .all()
        )
        context["tasks"] = task_statuses

        passed_tasks = []
        unfinished_tasks = []
        for status in task_statuses:
            if status.is_done:
                passed_tasks.append(str(status.task.number))
            else:
                unfinished_tasks.append(str(status.task.number))
        context["passed_tasks"] = ", ".join(passed_tasks)
        context["unfinished_tasks"] = ", ".join(unfinished_tasks)

        return context
