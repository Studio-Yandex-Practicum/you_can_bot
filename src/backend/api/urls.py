from django.urls import path
from .views import answer_create


urlpatterns = [
    path(
        'v1/users/<int:telegram_id>/tasks/<int:task_number>/answers/',
        answer_create,
        name='answer_create'),
]
