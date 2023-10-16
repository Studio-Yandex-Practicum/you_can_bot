from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password
from django.db import transaction

from api.models import MentorProfile, User, UserFromTelegram


class BaseCaseForProblemTests(APITestCase):
    """Базовый набор констант для тестов модуля api."""

    TELEGRAM_ID = 1234567
    MENTOR_TELEGRAM_ID = 7654321
    UNKNOWN_USER_TELEGRAM_ID = 7654321
    TELEGRAM_USERNAME = "hasnoname"
    TELEGRAM_NAME = "HasNoName"
    TELEGRAM_SURNAME = "HasNoSurname"
    MESSAGE = "Как дела?"
    EMPTY_MESSAGE_1 = ""
    EMPTY_MESSAGE_2 = " "
    DJANGO_USERNAME = "username"
    DJANGO_USER_PASSWORD = "password"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with transaction.atomic():
            cls.user = User.objects.create_user(
                username=cls.DJANGO_USERNAME,
            )
            cls.user.mentorprofile.telegram_id = cls.MENTOR_TELEGRAM_ID
            cls.user.mentorprofile.save()
            cls.user_from_telegram = UserFromTelegram.objects.create(
                telegram_id=cls.TELEGRAM_ID,
                telegram_username=cls.TELEGRAM_USERNAME,
                name=cls.TELEGRAM_NAME,
                surname=cls.TELEGRAM_SURNAME,
                mentor=cls.user.mentorprofile,
            )
