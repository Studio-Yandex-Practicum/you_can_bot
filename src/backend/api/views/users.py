from rest_framework import mixins, viewsets

from api.models import UserFromTelegram
from api.serializers import UserFromTelegramRetrieveCreateSerializer, \
    UserFromTelegramUpdateSerializer


class UserFromTelegramViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Вьюсет для обработки запросов, связанных с пользователем telegram.
    Доступные HTTP методы: GET, POST, PATCH.
    Поле для detail-запросов: telegram_id.
    """

    queryset = UserFromTelegram.objects.all()
    http_method_names = ["get", "post", "patch"]
    lookup_field = "telegram_id"

    def get_serializer_class(self):
        if self.action == "partial_update":
            return UserFromTelegramUpdateSerializer
        return UserFromTelegramRetrieveCreateSerializer
