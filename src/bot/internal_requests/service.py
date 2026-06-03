import asyncio
import logging
import os
from dataclasses import asdict
from typing import List, Optional, Type, TypeVar, Union
from urllib.parse import urljoin

import httpx
from httpx import AsyncClient, Response

from internal_requests.entities import (
    Answer,
    Mentor,
    MentorRegistered,
    MentorRegistrationStatus,
    Message,
    Problem,
    Task,
    TaskStatus,
    UserFromTelegram,
)

_LOGGER = logging.getLogger(__name__)

Model = TypeVar("Model")

INTERNAL_API_URL = os.getenv("INTERNAL_API_URL", "http://127.0.0.1:8000/api/v1/")
DEFAULT_READ_TIMEOUT_SECONDS = 15.0

REQUEST_MAX_ATTEMPTS = 3
REQUEST_INITIAL_DELAY_SECONDS = 1.0


def _read_timeout_from_env() -> float:
    """Read INTERNAL_API_TIMEOUT, falling back to the default on bad values."""
    raw_value = os.getenv("INTERNAL_API_TIMEOUT")
    if raw_value is None:
        return DEFAULT_READ_TIMEOUT_SECONDS
    try:
        return float(raw_value)
    except ValueError:
        _LOGGER.warning(
            "Ignoring invalid INTERNAL_API_TIMEOUT=%r, using default %.1fs",
            raw_value,
            DEFAULT_READ_TIMEOUT_SECONDS,
        )
        return DEFAULT_READ_TIMEOUT_SECONDS


INTERNAL_API_READ_TIMEOUT = _read_timeout_from_env()

_TIMEOUT = httpx.Timeout(
    connect=5.0, read=INTERNAL_API_READ_TIMEOUT, write=10.0, pool=5.0
)
_LIMITS = httpx.Limits(max_keepalive_connections=10, max_connections=20)

_client: Optional[AsyncClient] = None


def _get_client() -> AsyncClient:
    """Return the shared AsyncClient, creating it lazily on first use.

    No lock is needed: the check and assignment below have no await between
    them and AsyncClient() is a synchronous constructor, so the asyncio event
    loop cannot switch tasks mid-initialization and create a second client.
    """
    global _client
    if _client is None:
        _client = AsyncClient(timeout=_TIMEOUT, limits=_LIMITS)
    return _client


async def get_messages_with_question(
    task_number: int, question_number: int
) -> List[Message]:
    """Получение сообщения с содержанием вопроса."""
    endpoint_urn = f"task/{task_number}/question/{question_number}/"
    response = await _get_request(endpoint_urn)
    messages = await _parse_api_response_to_messages(response)
    return messages


async def get_messages_with_results(
    telegram_id: int, task_number: int
) -> List[Message]:
    """Получение сообщения с расшифровкой."""
    endpoint_urn = f"users/{telegram_id}/tasks/{task_number}/results/"
    response = await _get_request(endpoint_urn)
    messages = await _parse_api_response_to_messages(response)
    return messages


async def get_info_about_user(telegram_id: int) -> UserFromTelegram:
    """Получения информации о пользователе из БД."""
    endpoint_urn = f"users/{telegram_id}/"
    response = await _get_request(endpoint_urn)
    user_info = await _parse_api_response_to_user_info(response)
    return user_info


async def update_user_info(telegram_id: int, data: dict):
    """Обновление информации о пользователе.

    PATCH-эндпоинт идемпотентен: DRF partial_update присваивает поля
    (name/surname) существующей записи без счётчиков и побочных эффектов
    (см. backend api/views/users.py), поэтому он помечен idempotent=True
    и безопасен для повтора того же payload.
    """
    endpoint_run = f"users/{telegram_id}/"
    response = await _patch_request(data, endpoint_run, idempotent=True)
    user_info_updated = await _parse_api_response_to_user_info(response)
    return user_info_updated


async def get_task_info_by_number(task_number: int) -> Task:
    """Получение информации о конкретном задании."""
    endpoint_urn = f"tasks/{task_number}/"
    response = await _get_request(endpoint_urn)
    result = await _parse_api_response_to_task_info(response)
    return result


async def get_task_info_list() -> List[Task]:
    """Получение списка заданий."""
    endpoint_urn = "tasks/"
    response = await _get_request(endpoint_urn)
    results = await _parse_api_response_to_task_info(response)
    return results


async def get_user_task_status_by_number(
    task_number: int, telegram_id: int
) -> TaskStatus:
    """Получение информации о конкретном статусе задания пользователя."""
    endpoint_urn = f"users/{telegram_id}/tasks/{task_number}/"
    response = await _get_request(endpoint_urn)
    result = await _parse_api_response_to_task_status(response)
    return result


async def get_user_task_status_list(telegram_id: int) -> List[TaskStatus]:
    """Получение списка статусов заданий пользователя."""
    endpoint_urn = f"users/{telegram_id}/tasks/"
    response = await _get_request(endpoint_urn)
    task_statuses = await _parse_api_response_to_task_status(response)
    return task_statuses


async def get_mentor_registration_status(telegram_id: int) -> MentorRegistrationStatus:
    """Получение информации о статусе регистрации профдизайнера."""
    endpoint_urn = f"mentors/{telegram_id}/status/"
    response = await _get_request(endpoint_urn)
    registrations_status = await _parse_api_response_to_mentor_registration_status(
        response
    )
    return registrations_status


async def create_user(user: UserFromTelegram) -> Response:
    """Запрос на занесение пользователя в БД."""
    data = asdict(user)
    endpoint_urn = "users/"
    response = await _post_request(data, endpoint_urn)
    return response


async def create_mentor(mentor: Mentor) -> MentorRegistered:
    """Запрос на создание учетной записи профдизайнера в БД."""
    data = asdict(mentor)
    endpoint_urn = "mentors/"
    response = await _post_request(data, endpoint_urn)
    mentor_registered = await _parse_api_response_to_mentor_info(response)
    return mentor_registered


async def confirm_mentor_registration(telegram_id: int) -> Response:
    """Запрос, подтверждающий учетную запись профдизайнера."""
    endpoint_urn = f"mentors/{telegram_id}/confirm/"
    response = await _post_request(dict(), endpoint_urn)
    return response


async def delete_mentor(telegram_id: int) -> Response:
    """Запрос на удаление учетной записи профдизайнера."""
    endpoint_urn = f"mentors/{telegram_id}/"
    response = await _delete_request(endpoint_urn)
    return response


async def create_question_from_user(problem: Problem) -> Response:
    """Запрос на занесение вопроса от пользователя в БД.

    Эндпоинт problems/ НЕ идемпотентен: на каждый вызов он создаёт новую
    запись Problem и шлёт уведомление ментору (см. backend
    api/views/problems.py), поэтому этот POST не повторяется.
    """
    data = asdict(problem)
    endpoint_urn = f"users/{problem.telegram_id}/problems/"
    response = await _post_request(data, endpoint_urn)
    return response


async def create_answer(answer: Answer) -> Response:
    """Запрос на занесение ответа от пользователя на вопрос задания.

    Эндпоинт answers/ идемпотентен: существующий ответ на тот же вопрос
    обновляется, а не дублируется (см. backend api/views/answer.py),
    поэтому он помечен idempotent=True и безопасен для повтора.
    """
    endpoint_urn = f"users/{answer.telegram_id}/tasks/{answer.task_number}/answers/"
    response = await _post_request(
        {"number": answer.number, "content": answer.content},
        endpoint_urn,
        idempotent=True,
    )
    return response


async def get_task_8_question(question_number: int, params: List) -> List[Message]:
    """Запрос на получение вопроса по 8-му заданию."""
    endpoint_urn = f"task_8_question/{question_number}/"
    response = await _get_request_with_params(endpoint_urn, params)
    messages = await _parse_api_response_to_messages(response=response)
    return messages


async def _get_request_with_params(endpoint_url: str, params) -> Response:
    return await _request("GET", endpoint_url, json=params, idempotent=True)


async def _get_request(endpoint_url: str) -> Response:
    return await _request("GET", endpoint_url, idempotent=True)


async def _post_request(
    data: dict, endpoint_url: str, idempotent: bool = False
) -> Response:
    return await _request("POST", endpoint_url, json=data, idempotent=idempotent)


async def _patch_request(
    data: dict, endpoint_url: str, idempotent: bool = False
) -> Response:
    return await _request("PATCH", endpoint_url, json=data, idempotent=idempotent)


async def _delete_request(endpoint_url: str, idempotent: bool = False) -> Response:
    return await _request("DELETE", endpoint_url, idempotent=idempotent)


async def _request(
    method: str,
    endpoint_url: str,
    json=None,
    idempotent: bool = False,
) -> Response:
    """Send a request through the shared client, retrying transient failures.

    Retries are attempted only for safe-to-repeat calls: every GET, and any
    non-GET method explicitly marked as idempotent. Retryable failures are
    transport errors (connect/read timeouts, etc.) and 5xx responses; 4xx and
    successful responses are returned without retry.
    """
    url = urljoin(base=INTERNAL_API_URL, url=endpoint_url)
    for attempt in range(1, REQUEST_MAX_ATTEMPTS + 1):
        is_last_attempt = attempt == REQUEST_MAX_ATTEMPTS
        try:
            response = await _get_client().request(method=method, url=url, json=json)
        except httpx.TransportError as error:
            if not idempotent or is_last_attempt:
                raise
            await _wait_before_retry(method, endpoint_url, attempt, repr(error))
            continue
        if _should_retry_response(response) and idempotent and not is_last_attempt:
            await _wait_before_retry(
                method, endpoint_url, attempt, f"status {response.status_code}"
            )
            continue
        response.raise_for_status()
        return response


def _should_retry_response(response: Response) -> bool:
    """Return whether the response status code warrants a retry (5xx only)."""
    return response.status_code >= 500


async def _wait_before_retry(
    method: str, endpoint_url: str, attempt: int, reason: str
) -> None:
    """Log a warning and sleep with exponential backoff before the next attempt."""
    delay = REQUEST_INITIAL_DELAY_SECONDS * 2 ** (attempt - 1)
    _LOGGER.warning(
        "Transient failure on %s %s (%s), attempt %d/%d, retrying in %.1fs",
        method,
        endpoint_url,
        reason,
        attempt,
        REQUEST_MAX_ATTEMPTS,
        delay,
    )
    await asyncio.sleep(delay)


async def _parse_api_response_to_messages(response: Response) -> List[Message]:
    json_response = response.json()
    result = json_response.get("result", [])
    messages = []
    for item in result:
        content = item.get("content", "")
        photo = item.get("photo", "")
        message = Message(content=content, photo=photo)
        messages.append(message)
    return messages


async def _parse_api_response_to_user_info(response: Response) -> UserFromTelegram:
    """Парсит полученный json из Response в датакласс UserFromTelegram."""
    return UserFromTelegram(**response.json())


async def _parse_api_response_to_mentor_info(response: Response) -> MentorRegistered:
    """Парсит полученный json из Response в датакласс MentorRegistered."""
    return MentorRegistered(**response.json())


async def _parse_api_response_to_mentor_registration_status(
    response: Response,
) -> MentorRegistrationStatus:
    """Парсит полученный json из Response в датакласс MentorRegistrationStatus."""
    return MentorRegistrationStatus(**response.json())


async def _parse_api_response_to_model(
    response: Response, model_class: Type[Model]
) -> Union[Model, List[Model]]:
    """Парсит полученный json из Response в экземпляр(ы) указанной модели."""
    json_response = response.json()
    instances = []

    if isinstance(json_response, list):
        for item_info in json_response:
            instance = model_class(**item_info)
            instances.append(instance)
    else:
        instance = model_class(**json_response)
        return instance
    return instances


async def _parse_api_response_to_task_status(
    response: Response,
) -> Union[TaskStatus, List[TaskStatus]]:
    """Парсит полученный json из Response в экземпляр(ы) TaskStatus."""
    return await _parse_api_response_to_model(response, TaskStatus)


async def _parse_api_response_to_task_info(
    response: Response,
) -> Union[Task, List[Task]]:
    """Парсит полученный json из Response в экземпляр(ы) Task."""
    return await _parse_api_response_to_model(response, Task)
