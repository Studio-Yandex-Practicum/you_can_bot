from rest_framework import serializers

from .models import UserFromTelegram


class UserFromTelegramRetrieveCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели `UserFromTelegram`.
    Используется для:
    - Получения информации по telegram_id (GET);
    - Создания новой записи в модель `UserFromTelegram` (POST).
    """

    class Meta:
        model = UserFromTelegram
        fields = ('telegram_id', 'telegram_username', 'name', 'surname')
        extra_kwargs = {
            'telegram_username': {'write_only': True}
        }


class UserFromTelegramUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели `UserFromTelegram`.
    Используется для:
    - Изменения полей name и surname в объекте модели UserFromTelegram.
    """

    class Meta:
        model = UserFromTelegram
        fields = ('telegram_id', 'name', 'surname')
        read_only_fields = ('telegram_id',)
