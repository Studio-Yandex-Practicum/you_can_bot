from dataclasses import asdict
import logging
from urllib.parse import urljoin

from httpx import AsyncClient, Response

from internal_requests.entities import (
    Answer, Problem, UserFromTelegram, TaskStatus, Message)
from utils.configs import INTERNAL_API_URL

_LOGGER = logging.getLogger(__name__)


async def get_message_with_question(task: TaskStatus) -> Response:
    endpoint_urn = f"task/{task.task_number}/question/{task.question_number}/"
    response = await _get_request(endpoint_urn)
    return response.text

  
async def create_user(user: UserFromTelegram) -> Response:
    """Создания пользователя."""
    data = asdict(user)
    endpoint_urn = "users/"
    response = await _post_request(data, endpoint_urn)
    return response


async def create_question_from_user(problem: Problem) -> Response:
    """Создания вопроса от пользователя"""
    data = asdict(problem)
    endpoint_urn = f"users/{problem.telegram_id}/problems/"
    response = await _post_request(data, endpoint_urn)
    return response


async def create_answer(answer: Answer) -> Response:
    """Создания вопроса от пользователя"""
    data = asdict(answer)
    endpoint_urn = f"users/{answer.telegram_id}/problems/"
    response = await _post_request(data, endpoint_urn)
    return response


async def _get_request(endpoint_urn: str) -> Response:
    async with AsyncClient() as client:
        response = client.get(
            url=urljoin(
                base=INTERNAL_API_URL,
                url=endpoint_urn,
            )
        )
    await _log_get_response(response)


async def _log_get_response(response: Response) -> None:
    if response.status_code == 200:
        _LOGGER.debug("Запрос успешен.")
    else:
        _LOGGER.error("Запрос не успешен.")


async def _post_request(data: dict, endpoint_urn: str) -> Response:
    async with AsyncClient() as client:
        response = client.post(
            url=urljoin(
                base=INTERNAL_API_URL,
                url=endpoint_urn,
            ),
            json=data,
        )
    await _log_post_response(data, response)
    return response


async def _log_post_response(data: dict, response: Response) -> None:
    if response.is_success:
        _LOGGER.debug(f"Запрос успешен. Входные данные: {data}")
    else:
        _LOGGER.error(
            f"Запрос неудачен. Входные данные: {data}"
            f" Ответ сервера: {response.status_code} {response.text}"
        )