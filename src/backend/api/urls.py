from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserFromTelegramViewSet, answer_create

app_name = "api"

router = DefaultRouter()
router.register(r"users", UserFromTelegramViewSet, basename="users")

urlpatterns = [
    path("v1/", include(router.urls)),
    path(
        "v1/users/<int:telegram_id>/tasks/<int:task_number>/answers/",
        answer_create,
        name="answer_create",
    ),
]
