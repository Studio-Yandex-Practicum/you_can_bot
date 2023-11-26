from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from api.serializers import MentorSerializer

User = get_user_model()


ACCOUNT_CONFIRMED = "Учетная запись подтверждена."


class MentorViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    Вьюсет для управления учетными записями профдизайнеров.
    Поле для detail-запросов: telegram_id связанной модели MentorProfile.
    """

    queryset = User.objects.all()
    serializer_class = MentorSerializer
    http_method_names = ("get", "head", "options", "post", "delete")
    lookup_field = "mentorprofile__telegram_id"

    @action(("get",), detail=True)
    def status(self, request, mentorprofile__telegram_id):
        """
        Эндпоинт для получения информации о статусе регистрации профдизайнера.

        В возращаемом эндпоинтом json содержится два поля с булевыми значениями:
        - registered: True для зарегистрированного пользователя;
        или False для несуществующей учетной записи.
        - confirmed: True для пользователя с атрибутом is_staff=True;
        или False для пользователя с атрибутом is_staff=False (либо
        несуществующей учетной записи).
        """
        mentor = User.objects.filter(
            mentorprofile__telegram_id=mentorprofile__telegram_id
        )
        registered = mentor.exists()
        data = {
            "registered": registered,
            "confirmed": registered and mentor.first().is_staff,
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @action(("post",), detail=True)
    def confirm(self, request, mentorprofile__telegram_id):
        """
        Эндпоинт для подтверждения учетной записи пользователя.
        Устанваливает атрибут is_staff экземляра User в значение True.
        """
        mentor = _get_mentor_or_404(mentorprofile__telegram_id)
        if mentor.is_staff is False:
            mentor.is_staff = True
            mentor.save()
        return Response(data={"info": ACCOUNT_CONFIRMED}, status=status.HTTP_200_OK)


def _get_mentor_or_404(telegram_id):
    """
    Возвращает экземпляр модели User, для которого в связанном
    объекте модели MentorProfile значение telegram_id равно переданному.
    Если объект отсутствует, вызывается исключение NotFound.
    """
    try:
        mentor = User.objects.get(mentorprofile__telegram_id=telegram_id)
    except User.DoesNotExist:
        raise NotFound(detail=settings.NOT_FOUND_MENTOR_MESSAGE)
    return mentor
