import logging
import os
from dataclasses import asdict
from typing import List, Union
from urllib.parse import urljoin

from httpx import AsyncClient, Response

from internal_requests.entities import (
    Answer,
    Mentor,
    MentorRegistered,
    MentorRegistrationStatus,
    Message,
    Problem,
    TaskStatus,
    UserFromTelegram,
)

_LOGGER = logging.getLogger(__name__)

INTERNAL_API_URL = os.getenv("INTERNAL_API_URL", "http://127.0.0.1:8000/api/v1/")


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
    endpoint_run = f"users/{telegram_id}/"
    response = await _patch_request(data, endpoint_run)
    user_info_updated = await _parse_api_response_to_user_info(response)
    return user_info_updated


async def get_user_task_status_by_number(
    task_number: int, telegram_id: int
) -> TaskStatus:
    """Получение информации о конкретном статусе задания пользователя."""
    endpoint_urn = f"users/{telegram_id}/tasks/{task_number}/"
    response = await _get_request(endpoint_urn)
    results = await _parse_api_response_to_task_status(response)
    return results[0]


async def get_user_task_status_list(telegram_id: int) -> List[TaskStatus]:
    """Получение списка статусов заданий пользователя."""
    endpoint_urn = f"users/{telegram_id}/tasks/"
    response = await _get_request(endpoint_urn)
    task_statuses = await _parse_api_response_to_task_status(response)
    return task_statuses


async def get_mentor_registration_status(telegram_id: int) -> MentorRegistrationStatus:
    """Получение информации о статусе регистрации психолога."""
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
    """Запрос на создание учетной записи психолога в БД."""
    data = asdict(mentor)
    endpoint_urn = "mentors/"
    response = await _post_request(data, endpoint_urn)
    mentor_registered = await _parse_api_response_to_mentor_info(response)
    return mentor_registered


async def confirm_mentor_registration(telegram_id: int) -> Response:
    """Запрос, подтверждающий учетную запись психолога."""
    endpoint_urn = f"mentors/{telegram_id}/confirm/"
    response = await _post_request(dict(), endpoint_urn)
    return response


async def delete_mentor(telegram_id: int) -> Response:
    """Запрос на удаление учетной записи психолога."""
    endpoint_urn = f"mentors/{telegram_id}/"
    response = await _delete_request(endpoint_urn)
    return response


async def create_question_from_user(problem: Problem) -> Response:
    """Запрос на занесение вопроса от пользователя в БД."""
    data = asdict(problem)
    endpoint_urn = f"users/{problem.telegram_id}/problems/"
    response = await _post_request(data, endpoint_urn)
    return response


async def create_answer(answer: Answer) -> Response:
    """Запрос на занесение ответа от пользователя на вопрос задания."""
    endpoint_urn = f"users/{answer.telegram_id}/tasks/{answer.task_number}/answers/"
    response = await _post_request(
        {"number": answer.number, "content": answer.content}, endpoint_urn
    )
    return response


async def _get_request(endpoint_url: str) -> Response:
    async with AsyncClient() as client:
        response = await client.get(
            url=urljoin(
                base=INTERNAL_API_URL,
                url=endpoint_url,
            )
        )
    response.raise_for_status()
    return response


async def _post_request(data: dict, endpoint_url: str) -> Response:
    async with AsyncClient() as client:
        response = await client.post(
            url=urljoin(
                base=INTERNAL_API_URL,
                url=endpoint_url,
            ),
            json=data,
        )
    response.raise_for_status()
    return response


async def _patch_request(data: dict, endpoint_url: str) -> Response:
    async with AsyncClient() as client:
        response = await client.patch(
            url=urljoin(
                base=INTERNAL_API_URL,
                url=endpoint_url,
            ),
            json=data,
        )
    response.raise_for_status()
    return response


async def _delete_request(endpoint_url: str) -> Response:
    async with AsyncClient() as client:
        response = await client.delete(
            url=urljoin(
                base=INTERNAL_API_URL,
                url=endpoint_url,
            )
        )
    response.raise_for_status()
    return response


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


async def _parse_api_response_to_task_status(
    response: Response,
) -> Union[TaskStatus, List[TaskStatus]]:
    """Парсит полученный json из Response в экземпляр(ы) TaskStatus."""
    json_response = response.json()
    tasks = []
    if isinstance(json_response, list):
        for task_info in json_response:
            task = TaskStatus(**task_info)
            tasks.append(task)
    else:
        task = TaskStatus(**json_response)
        tasks.append(task)
    return tasks
