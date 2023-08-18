from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    verbose_name = "База данных сервиса You_can_bot"

    def ready(self):
        from . import signals  # noqa
