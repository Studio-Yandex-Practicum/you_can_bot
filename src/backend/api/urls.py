from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views.answer import answer_create
from api.views.tasks import TasksViewSet
from api.views.problems import problem_create
from api.views.users import UserFromTelegramViewSet

app_name = "api"

router = DefaultRouter()

router.register(r"users", UserFromTelegramViewSet, basename="users")
router.register(r"users/(?P<telegram_id>\d+)/tasks", TasksViewSet, basename="tasks")

urlpatterns = [
    path("v1/", include(router.urls)),
    path(
        "v1/users/<int:telegram_id>/problems/",
        problem_create,
        name="problem_create",
    ),
    path(
        "v1/users/<int:telegram_id>/tasks/<int:task_number>/answers/",
        answer_create,
        name="answer_create",
    ),
]
