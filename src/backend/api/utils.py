from random import randint

from django.contrib.auth import get_user_model
from slugify import slugify

User = get_user_model()


def create_available_username(first_name: str, last_name: str) -> str:
    """Создает доступный username пользователя из имени и фамилии."""
    full_name = " ".join([first_name, last_name])
    username = slugify(full_name)
    while User.objects.filter(username=username).exists():
        username += str(randint(1, 9))
    return username
