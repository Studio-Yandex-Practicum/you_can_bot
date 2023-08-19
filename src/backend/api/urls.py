from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserFromTelegramViewSet

app_name = 'api'

router = DefaultRouter()

router.register(r'users', UserFromTelegramViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
