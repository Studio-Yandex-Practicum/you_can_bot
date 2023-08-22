import json

from django.contrib.auth import get_user

from api.tests.test_case import BaseCaseForTests


class ViewTests(BaseCaseForTests):
    """Проверка контроллеров view модуля api."""

    def test_view_answer_create(self):
        """Проверка контроллера answer_create."""
        ...
