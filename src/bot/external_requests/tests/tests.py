from http.client import FORBIDDEN, NOT_FOUND
from unittest.mock import MagicMock, Mock, patch

from httpx import AsyncClient, HTTPStatusError, Request, RequestError, Response, codes

from ..exceptions import APIForbiddenError, PostAPIError, UserNotFound
from ..service import TARIFFS, get_user_info_from_lk
from .fixtures import CaseForGetUserInfoFromLK


class TestGetUserInfoFromLK(CaseForGetUserInfoFromLK):
    def setUp(self) -> None:
        self.response = MagicMock()
        self.response.status_code = codes.OK

    def set_post_request(
        self, post_request: Mock, exception: Exception, **kwargs
    ) -> None:
        """Мок с переданным исключением, сообщением и ответом.
        ### Args:
        - post_request (Mock):
            Мок
        - exception (Exception):
            исключение, которое нужно бросить
        ### Kwargs:
        - message (str):
            сообщение исключения
        - response (Response):
            подменяемый ответ сервера
        """
        post_request.side_effect = MagicMock(
            side_effect=exception(request=Request("POST", self.FAKE_URL), **kwargs)
        )

    async def assert_equal_from_sequence(
        self, post_request: Mock, compared_values
    ) -> None:
        """Шаблон для вызова assertEqual из последовательности.
        ### Args:
        - post_request (Mock):
            Мок
        - compared_values:
          последовательность кортежей с подменяемыми объектами
          и ожидаемыми значениями.
        """
        for mocked, expected in compared_values:
            with self.subTest(mocked=mocked, expected=expected):
                post_request.return_value = mocked
                user_info = await get_user_info_from_lk(self.TELEGRAM_ID)
                self.assertEqual(user_info, expected)

    async def assert_raises_from_sequence(
        self, post_request: Mock, compared_values
    ) -> None:
        """Шаблон для вызова assertRaises из последовательности.
        ### Args:
        - post_request (Mock):
            Мок
        - compared_values:
          последовательность кортежей с подменяемыми объектами
          и ожидаемыми исключениями.
        """
        for mocked, exception in compared_values:
            with self.subTest(mocked=mocked, exception=exception):
                post_request.return_value = mocked
                with self.assertRaises(exception):
                    await get_user_info_from_lk(self.TELEGRAM_ID)

    @patch.object(AsyncClient, "post")
    async def test_403_http_error(self, post_request):
        """Тест ошибки 403 Forbidden."""
        self.set_post_request(
            post_request=post_request,
            exception=HTTPStatusError,
            message=self.MESSAGE_403_FORBIDDEN,
            response=Response(FORBIDDEN),
        )
        with self.assertRaises(APIForbiddenError):
            await get_user_info_from_lk(self.TELEGRAM_ID)

    @patch.object(AsyncClient, "post")
    async def test_404_http_error(self, post_request):
        """Тест ошибки 404 Not Found."""
        self.set_post_request(
            post_request=post_request,
            exception=HTTPStatusError,
            message=self.MESSAGE_404_NOT_FOUND,
            response=Response(NOT_FOUND),
        )
        with self.assertRaises(UserNotFound):
            await get_user_info_from_lk(self.TELEGRAM_ID)

    @patch.object(AsyncClient, "post")
    async def test_incorrect_json(self, post_request):
        """Тест отказа сервера с кодом code в json."""
        self.response.json = MagicMock(return_value=self.ERROR_CODE)
        await self.assert_raises_from_sequence(
            post_request, [(self.response, PostAPIError)]
        )

    async def test_incorrect_telegram_id(self):
        """Тест некорректного телеграм id."""
        with self.assertRaises(TypeError):
            await get_user_info_from_lk(self.STRING)
        with self.assertRaises(ValueError):
            await get_user_info_from_lk(self.NEGATIVE_NUMBER)

    @patch.object(AsyncClient, "post")
    async def test_incorrect_type_in_responce(self, post_request):
        """Тест некорректного содержания json."""
        self.response.json = MagicMock(return_value=self.STRING)
        await self.assert_raises_from_sequence(
            post_request, [(self.response, TypeError)]
        )

    @patch.object(AsyncClient, "post")
    async def test_request_error(self, post_request):
        """Тест сбоя сети."""
        self.set_post_request(
            post_request=post_request,
            exception=RequestError,
            message=self.MESSAGE_REQUEST_ERROR,
        )
        with self.assertRaises(ConnectionError):
            await get_user_info_from_lk(self.TELEGRAM_ID)

    @patch.object(AsyncClient, "post")
    async def test_success_request(self, post_request):
        """Тест успешного запроса."""
        self.response.json = MagicMock(return_value=self.SUCCESS_DATA)
        await self.assert_equal_from_sequence(
            post_request, [(self.response, self.SUCCESS_USER_INFO)]
        )

    @patch("external_requests.service._post_request")
    async def test_unexpected_full_name(self, post_request):
        """Тест неожиданных значений full_name."""
        await self.assert_equal_from_sequence(
            post_request,
            [
                (self.NO_SURNAME, self.RETURN_NO_SURNAME),
                (self.DOUBLE_SPACE_IN_NAME, self.RETURN_DOUBLE_SPACE_IN_NAME),
            ],
        )

    @patch("external_requests.service._post_request")
    async def test_upsent_json_keys(self, post_request):
        """Тест отсутствия ключей json."""
        await self.assert_raises_from_sequence(
            post_request,
            [
                (self.NO_IS_APPROVED, KeyError),
                (self.NO_FULL_NAME, KeyError),
                (self.NO_TARIFF, KeyError),
            ],
        )

    @patch("external_requests.service._post_request")
    async def test_unexpected_json_values(self, post_request):
        """Тест неожиданных значений json."""
        await self.assert_raises_from_sequence(
            post_request,
            [
                (self.UNEXPECTED_TYPE_ISAPPROVED, TypeError),
                (self.UNEXPECTED_TYPE_FULL_NAME, TypeError),
                (self.UNEXPECTED_TYPE_TARIFF, ValueError),
            ],
        )

    @patch.object(AsyncClient, "post")
    async def test_unexpected_status_code(self, post_request):
        """Тест неожиданного значения status_code."""
        self.response.status_code = self.UNEXPECTED_STATUS_CODE
        await self.assert_raises_from_sequence(
            post_request, [(self.response, PostAPIError)]
        )

    @patch("external_requests.service._post_request")
    async def test_tariff_value(self, post_request):
        """Тест значений tariff в json."""
        for value in [
            self.TARIFF_MAXI,
            self.TARIFF_MIDI,
            self.TARIFF_MINI,
            self.TARIFF_NONE,
        ]:
            post_request.return_value = value
            user_info = await get_user_info_from_lk(self.TELEGRAM_ID)
            self.assertIn(user_info["tariff"], TARIFFS)
