from rest_framework import mixins, viewsets

from .serializers import (
    UserFromTelegramRetrieveCreateSerializer,
    UserFromTelegramUpdateSerializer
)
from .models import UserFromTelegram


class UserFromTelegramViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    Вьюсет для обработки запросов, связанных с пользователем telegram.
    Доступные HTTP методы: GET, POST, PATCH.
    Поле для detail-запросов: telegram_id.
    """
    queryset = UserFromTelegram.objects.all()
    serializer_class = UserFromTelegramRetrieveCreateSerializer
    http_method_names = ['get', 'post', 'patch']
    lookup_field = 'telegram_id'

    def get_serializer_class(self):
        print(self.action)
        if self.action == 'partial_update':
            return UserFromTelegramUpdateSerializer
        return UserFromTelegramRetrieveCreateSerializer
