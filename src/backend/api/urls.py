from django.urls import path
from .views import create_question

urlpatterns = [
	path('api/v1/users/<str:telegram_id>/questions/', create_question),
]
