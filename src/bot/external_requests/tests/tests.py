from http.client import FORBIDDEN, NOT_FOUND
from unittest.mock import MagicMock, patch

from httpx import AsyncClient, HTTPStatusError, Request, RequestError, Response, codes

from ..exceptions import APIForbiddenError, PostAPIError, UserNotFound
from ..service import TARIFFS, get_user_info_from_lk
from .fixtures import CaseForGetUserInfoFromLK


class TestGetUserInfoFromLK(CaseForGetUserInfoFromLK):

    def setUp(self) -> None:
        self.response = MagicMock()

    def set_mock(
        self,
        post_request: MagicMock,
        exception: Exception,
        **kwargs
    ):
        """Мок с переданным исключением, сообщением и ответом.
        ### Args:
        - post_request (MagicMock):
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
            side_effect=exception(request=Request('POST', self.FAKE_URL), **kwargs)
        )

    @patch.object(AsyncClient, 'post')
    async def test_403_http_error(self, post_request):
        """Тест ошибки 403 Forbidden."""
        self.set_mock(
            post_request=post_request,
            exception=HTTPStatusError,
            message=self.MESSAGE_403_FORBIDDEN,
            response=Response(FORBIDDEN)
        )
        with self.assertRaises(APIForbiddenError):
            await get_user_info_from_lk(self.TELEGRAM_ID)

    @patch.object(AsyncClient, 'post')
    async def test_404_http_error(self, post_request):
        """Тест ошибки 404 Not Found."""
        self.set_mock(
            post_request=post_request,
            exception=HTTPStatusError,
            message=self.MESSAGE_404_NOT_FOUND,
            response=Response(NOT_FOUND)
        )
        with self.assertRaises(UserNotFound):
            await get_user_info_from_lk(self.TELEGRAM_ID)

    @patch.object(AsyncClient, 'post')
    async def test_incorrect_json(self, post_request):
        """Тест отказа сервера с кодом code в json."""
        self.response.status_code = codes.OK
        self.response.json = MagicMock(return_value=self.ERROR_JSON)
        post_request.return_value = self.response
        with self.assertRaises(PostAPIError):
            await get_user_info_from_lk(self.TELEGRAM_ID)

    async def test_incorrect_telegram_id(self):
        """Тест некорректного телеграм id."""
        with self.assertRaises(TypeError):
            await get_user_info_from_lk(self.STRING)
        with self.assertRaises(ValueError):
            await get_user_info_from_lk(self.NEGATIVE_INT)

    @patch.object(AsyncClient, 'post')
    async def test_incorrect_type_in_responce(self, post_request):
        """Тест некорректного содержания json."""
        self.response.status_code = codes.OK
        self.response.json = MagicMock(return_value=self.STRING)
        post_request.return_value = self.response
        with self.assertRaises(TypeError):
            await get_user_info_from_lk(self.TELEGRAM_ID)

    @patch.object(AsyncClient, 'post')
    async def test_request_error(self, post_request):
        """Тест сбоя сети."""
        self.set_mock(
            post_request=post_request,
            exception=RequestError,
            message=self.MESSAGE_REQUEST_ERROR
        )
        with self.assertRaises(ConnectionError):
            await get_user_info_from_lk(self.TELEGRAM_ID)

    @patch.object(AsyncClient, 'post')
    async def test_success_request(self, post_request):
        """Тест успешного запроса."""
        self.response.status_code = codes.OK
        self.response.json = MagicMock(return_value=self.SUCCESS_JSON)
        post_request.return_value = self.response
        user_info = await get_user_info_from_lk(self.TELEGRAM_ID)
        self.assertEqual(user_info, self.SUCCESS_USER_INFO)

    @patch('external_requests.service._post_request')
    async def test_unexpected_full_name(self, post_request):
        """Тест неожиданных значений full_name."""
        post_request.return_value = self.JSON_WITHOUT_SURNAME
        user_info = await get_user_info_from_lk(self.TELEGRAM_ID)
        self.assertEqual(user_info, self.RETURN_WITHOUT_SURNAME)
        post_request.return_value = self.JSON_WITH_DOUBLE_SPACE_IN_NAME
        user_info = await get_user_info_from_lk(self.TELEGRAM_ID)
        self.assertEqual(user_info, self.RETURN_WITH_DOUBLE_SPACE_IN_NAME)

    @patch('external_requests.service._post_request')
    async def test_upsent_json_keys(self, post_request):
        """Тест отсутствия ключей json."""
        post_request.return_value = self.JSON_WITHOUT_TARIFF
        with self.assertRaises(KeyError):
            await get_user_info_from_lk(self.TELEGRAM_ID)
        post_request.return_value = self.JSON_WITHOUT_FULL_NAME
        with self.assertRaises(KeyError):
            await get_user_info_from_lk(self.TELEGRAM_ID)
        post_request.return_value = self.JSON_WITHOUT_ISAPPROVED
        with self.assertRaises(KeyError):
            await get_user_info_from_lk(self.TELEGRAM_ID)

    @patch('external_requests.service._post_request')
    async def test_unexpected_json_values(self, post_request):
        """Тест неожиданных значений json."""
        post_request.return_value = self.JSON_UNEXPECTED_TYPE_TARIFF
        with self.assertRaises(ValueError):
            await get_user_info_from_lk(self.TELEGRAM_ID)
        post_request.return_value = self.JSON_UNEXPECTED_TYPE_FULL_NAME
        with self.assertRaises(TypeError):
            await get_user_info_from_lk(self.TELEGRAM_ID)
        post_request.return_value = self.JSON_UNEXPECTED_TYPE_ISAPPROVED
        with self.assertRaises(TypeError):
            await get_user_info_from_lk(self.TELEGRAM_ID)

    @patch.object(AsyncClient, 'post')
    async def test_unexpected_status_code(self, post_request):
        """Тест неожиданных значений status_code."""
        self.response.status_code = self.UNEXPECTED_STATUS_CODE
        post_request.return_value = self.response
        with self.assertRaises(PostAPIError):
            await get_user_info_from_lk(self.TELEGRAM_ID)

    @patch('external_requests.service._post_request')
    async def test_tariff(self, post_request):
        """Тест значений tariff в json."""
        post_request.return_value = self.JSON_TARIFF_MINI
        user_info = await get_user_info_from_lk(self.TELEGRAM_ID)
        self.assertIn(user_info['tariff'], TARIFFS)
        post_request.return_value = self.JSON_TARIFF_MIDI
        user_info = await get_user_info_from_lk(self.TELEGRAM_ID)
        self.assertIn(user_info['tariff'], TARIFFS)
        post_request.return_value = self.JSON_TARIFF_MAXI
        user_info = await get_user_info_from_lk(self.TELEGRAM_ID)
        self.assertIn(user_info['tariff'], TARIFFS)
        post_request.return_value = self.JSON_TARIFF_NONE
        user_info = await get_user_info_from_lk(self.TELEGRAM_ID)
        self.assertIn(user_info['tariff'], TARIFFS)
