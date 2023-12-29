from django.urls import path

from info_pages.views import UserDetailView

app_name = "info_pages"

urlpatterns = [
    path(
        "info/user/<int:telegram_id>/",
        UserDetailView.as_view(),
        name="taskstatus-list",
    ),
]
