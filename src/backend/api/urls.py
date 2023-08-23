from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TasksViewSet

app_name = "api"

router = DefaultRouter()

router.register(
    r"users/(?P<telegram_id>d+)/tasks", TasksViewSet, basename="tasks"
)
router.register(
    r"users/(?P<telegram_id>d+)/tasks/(?P<task_number>d+)",
    viewset=TasksViewSet,
    basename="task",
)

urlpatterns = [path("", include(router.urls))]
