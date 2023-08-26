from django.urls import path
from .views import create_question

urlpatterns = [
	path('api/v1/users/<int:telegram_id>/problems/', create_question),
]
