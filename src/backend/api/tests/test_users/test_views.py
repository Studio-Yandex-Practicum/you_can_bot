from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.models import UserFromTelegram


class UserTests(APITestCase):
    REQUEST_FORMAT = "json"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFromTelegram.objects.create(
            telegram_id=12345,
            telegram_username="username",
            name="Илья",
            surname="Юзеров",
        )

    def setUp(self):
        self.client = APIClient()

    @staticmethod
    def _get_detail_user_url(telegram_id: int) -> str:
        return reverse("api:users-detail", kwargs={"telegram_id": telegram_id})

    def test_create_tg_user(self):
        """Пользователь успешно создается через API."""
        new_user_data = {
            "telegram_id": 55555,
            "telegram_username": "newusername",
            "name": "Джон",
            "surname": "Смит",
        }
        expected_response_data = new_user_data.copy()
        expected_response_data.pop("telegram_username")
        count_of_users_before = UserFromTelegram.objects.count()

        response = self.client.post(
            reverse("api:users-list"), new_user_data, format=self.REQUEST_FORMAT
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response_data)
        self.assertEqual(count_of_users_before + 1, UserFromTelegram.objects.count())

    def test_get_tg_user(self):
        """Пользователь успешно получен по telegram_id через API."""
        count_of_users_before = UserFromTelegram.objects.count()
        response = self.client.get(
            self._get_detail_user_url(UserTests.user.telegram_id)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "telegram_id": UserTests.user.telegram_id,
                "name": UserTests.user.name,
                "surname": UserTests.user.surname,
            },
        )

        # Новый пользователь не создался при GET-запросе
        self.assertEqual(count_of_users_before, UserFromTelegram.objects.count())

        # Тестирование обращения к несуществующему telegram_id
        non_existent_user_telegram_id = 123
        response = self.client.get(
            self._get_detail_user_url(non_existent_user_telegram_id)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Новый пользователь не создался
        # при GET-запросе к несуществующему telegram_id
        self.assertEqual(count_of_users_before, UserFromTelegram.objects.count())

    def test_patch_tg_user(self):
        """У пользователя успешно изменилось имя и фамилия."""
        new_user_tg_id = 321
        new_user_username = "patchuser"

        new_user = UserFromTelegram.objects.create(
            telegram_id=new_user_tg_id,
            telegram_username=new_user_username,
            name="Имя",
            surname="Фамилия",
        )
        count_of_users_before = UserFromTelegram.objects.count()

        new_name = "Новое имя"
        new_surname = "Новая фамилия"
        new_tg_id_try = 666
        new_object_id_try = 444
        new_tg_username_try = "newestusername"

        response = self.client.patch(
            self._get_detail_user_url(new_user.telegram_id),
            {
                "name": new_name,
                "surname": new_surname,
                "telegram_id": new_tg_id_try,
                "id": new_object_id_try,
                "telegram_username": new_tg_username_try,
            },
            format=self.REQUEST_FORMAT,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"telegram_id": new_user_tg_id, "name": new_name, "surname": new_surname},
        )
        self.assertEqual(count_of_users_before, UserFromTelegram.objects.count())

        # Нужные поля у нужного юзера были обновлены,
        # поля, которые не подлежат изменению, не были изменены.
        modified_user = UserFromTelegram.objects.get(telegram_id=new_user_tg_id)
        self.assertEqual(modified_user.name, new_name)
        self.assertEqual(modified_user.surname, new_surname)
        self.assertEqual(modified_user.telegram_username, new_user_username)
        self.assertEqual(modified_user.id, new_user.id)

    def test_requests_chain_tg_user(self):
        """Последовательные запросы к различным эндпоинтам юзера работают
        корректно."""
        expected_response_data = {"telegram_id": 999, "name": "a", "surname": "b"}
        request_data = expected_response_data.copy()
        request_data["telegram_username"] = "c"

        # Создаем нового юзера через эндпоинт создания
        response = self.client.post(
            reverse("api:users-list"), request_data, format=self.REQUEST_FORMAT
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response_data)

        new_user_url = self._get_detail_user_url(expected_response_data["telegram_id"])

        # Получаем нового пользователя через эндпоинт по telegram_id
        response = self.client.get(new_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response_data)

        # Изменяем нового пользователя
        new_name = "e"
        expected_response_data["name"] = new_name
        response = self.client.patch(
            new_user_url, {"name": new_name}, format=self.REQUEST_FORMAT
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response_data)
