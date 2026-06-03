import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

import httpx

from internal_requests import service


def _response(status_code: int) -> MagicMock:
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.raise_for_status = MagicMock()
    if status_code >= 400:
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "error", request=MagicMock(), response=response
        )
    return response


def _patch_client(request_mock: AsyncMock):
    client = MagicMock()
    client.request = request_mock
    return patch.object(service, "_get_client", return_value=client)


@patch.object(service.asyncio, "sleep", new=AsyncMock())
class RequestRetryTests(IsolatedAsyncioTestCase):
    """Поведение повторов общего внутреннего HTTP-клиента."""

    async def test_successful_request_returns_response(self):
        request = AsyncMock(return_value=_response(200))
        with _patch_client(request):
            result = await service._get_request("users/1/")

        self.assertEqual(result.status_code, 200)
        request.assert_awaited_once()

    async def test_retries_read_timeout_then_succeeds(self):
        request = AsyncMock(side_effect=[httpx.ReadTimeout("slow"), _response(200)])
        with _patch_client(request):
            result = await service._get_request("users/1/")

        self.assertEqual(result.status_code, 200)
        self.assertEqual(request.await_count, 2)

    async def test_retries_until_max_attempts_then_raises(self):
        request = AsyncMock(side_effect=httpx.ConnectError("down"))
        with _patch_client(request):
            with self.assertRaises(httpx.ConnectError):
                await service._get_request("users/1/")

        self.assertEqual(request.await_count, service.REQUEST_MAX_ATTEMPTS)

    async def test_retries_on_5xx_response(self):
        request = AsyncMock(side_effect=[_response(503), _response(200)])
        with _patch_client(request):
            result = await service._get_request("users/1/")

        self.assertEqual(result.status_code, 200)
        self.assertEqual(request.await_count, 2)

    async def test_does_not_retry_4xx_response(self):
        request = AsyncMock(return_value=_response(404))
        with _patch_client(request):
            with self.assertRaises(httpx.HTTPStatusError):
                await service._get_request("users/1/")

        request.assert_awaited_once()

    async def test_does_not_retry_non_idempotent_post(self):
        request = AsyncMock(side_effect=httpx.ReadTimeout("slow"))
        with _patch_client(request):
            with self.assertRaises(httpx.ReadTimeout):
                await service._post_request({"a": 1}, "problems/")

        request.assert_awaited_once()

    async def test_retries_idempotent_post(self):
        request = AsyncMock(side_effect=[httpx.ReadTimeout("slow"), _response(201)])
        with _patch_client(request):
            result = await service._post_request({"a": 1}, "answers/", idempotent=True)

        self.assertEqual(result.status_code, 201)
        self.assertEqual(request.await_count, 2)

    async def test_backoff_grows_exponentially_between_retries(self):
        request = AsyncMock(
            side_effect=[
                httpx.ReadTimeout("slow"),
                httpx.ReadTimeout("slow"),
                _response(200),
            ]
        )
        sleep = AsyncMock()
        with _patch_client(request), patch.object(service.asyncio, "sleep", new=sleep):
            result = await service._get_request("users/1/")

        self.assertEqual(result.status_code, 200)
        self.assertEqual([call.args[0] for call in sleep.await_args_list], [1.0, 2.0])


class IdempotencyWiringTests(IsolatedAsyncioTestCase):
    """Каждый вызывающий помечает свой запрос idempotent в соответствии с эндпоинтом."""

    @patch.object(service, "_request", new_callable=AsyncMock)
    async def test_create_answer_marks_request_idempotent(self, request_mock):
        answer = service.Answer(telegram_id=1, task_number=5, number=1, content="a")
        await service.create_answer(answer)

        self.assertTrue(request_mock.await_args.kwargs["idempotent"])

    @patch.object(service, "_request", new_callable=AsyncMock)
    async def test_create_question_is_not_idempotent(self, request_mock):
        problem = service.Problem(telegram_id=1, message="help")
        await service.create_question_from_user(problem)

        self.assertFalse(request_mock.await_args.kwargs.get("idempotent", False))

    @patch.object(service, "_request", new_callable=AsyncMock)
    async def test_update_user_info_marks_request_idempotent(self, request_mock):
        request_mock.return_value = _response(200)
        request_mock.return_value.json.return_value = {
            "telegram_id": 1,
            "telegram_username": "u",
            "name": "Ann",
            "surname": "Smith",
        }
        await service.update_user_info(1, {"name": "Ann"})

        self.assertTrue(request_mock.await_args.kwargs["idempotent"])


class SharedClientTests(IsolatedAsyncioTestCase):
    """Единственный экземпляр AsyncClient переиспользуется между вызовами."""

    def setUp(self):
        service._client = None

    def tearDown(self):
        service._client = None

    def test_get_client_returns_same_instance(self):
        first = service._get_client()
        second = service._get_client()

        self.assertIs(first, second)


if __name__ == "__main__":
    unittest.main()
