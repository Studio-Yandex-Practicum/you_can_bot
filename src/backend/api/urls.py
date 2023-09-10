from api.views.answer import answer_create
from api.views.results import get_results_for_user_by_task
from api.views.tasks import TasksViewSet
from api.views.users import UserFromTelegramViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = "api"

router = DefaultRouter()

router.register(r"users", UserFromTelegramViewSet, basename="users")
router.register(
    r"users/(?P<telegram_id>\d+)/tasks",
    TasksViewSet,
    basename="tasks"
)

urlpatterns = [
    path("v1/", include(router.urls)),
    path(
        "v1/users/<int:telegram_id>/tasks/<int:task_number>/answers/",
        answer_create,
        name="answer_create",
    ),
    path(
        "v1/users/<int:telegram_id>/tasks/<int:task_number>/results/",
        get_results_for_user_by_task,
        name="get_results_for_user_by_task",
    ),
]
