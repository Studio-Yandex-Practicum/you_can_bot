from logging import getLogger
from typing import Optional, TypedDict

from httpx import AsyncClient, Response
from httpx._status_codes import code

from external_requests.exceptions import TelegramIdError, UserNotFound
from utils.configs import (
    ALL_TARIFFS,
    ROBOTGURU_TOKEN,
    ROBOTGURU_URL,
    YOUCANBY_TOKEN,
    YOUCANBY_URL,
)

IS_APPROVED = "isApproved"
FIRST_NAME = "first_name"
LAST_NAME = "last_name"
TARIFF = "tariff"
USER_INFO_KEYS = (
    IS_APPROVED,
    FIRST_NAME,
    LAST_NAME,
    TARIFF,
)

TARIFF_PRIORITY = {}
for index, tariff in enumerate(ALL_TARIFFS):
    TARIFF_PRIORITY[tariff] = index


class UserInfo(TypedDict):
    isApproved: bool
    first_name: str
    last_name: str
    tariff: Optional[str]


_LOGGER = getLogger(__name__)


async def get_user_info_from_lk(telegram_id: int) -> Optional[UserInfo]:
    check_telegram_id(telegram_id)

    user_info_from_youcanby = await _get_user_info_from_youcanby(telegram_id)
    user_info_from_robotguru = await _get_user_info_from_robotguru(telegram_id)

    if user_info_from_youcanby is None and user_info_from_robotguru is None:
        raise UserNotFound()
    if user_info_from_youcanby is not None and user_info_from_robotguru is None:
        return user_info_from_youcanby
    if user_info_from_youcanby is None and user_info_from_robotguru is not None:
        return user_info_from_robotguru
    if (
        TARIFF_PRIORITY[user_info_from_youcanby[TARIFF]]
        >= TARIFF_PRIORITY[user_info_from_robotguru[TARIFF]]
    ):
        user_info = user_info_from_youcanby
    else:
        user_info = user_info_from_robotguru

    return user_info


def check_telegram_id(value: int) -> int:
    if not isinstance(value, int) or value <= 0:
        raise TelegramIdError("Chat ID должен быть положительным целым числом.")
    return value


async def _get_user_info_from_youcanby(telegram_id: int) -> Optional[UserInfo]:
    return await _post_request_to_lk_api(telegram_id, YOUCANBY_URL, YOUCANBY_TOKEN)


async def _get_user_info_from_robotguru(telegram_id: int) -> Optional[UserInfo]:
    return await _post_request_to_lk_api(telegram_id, ROBOTGURU_URL, ROBOTGURU_TOKEN)


async def _post_request_to_lk_api(
    telegram_id: int, url: str, token: str
) -> Optional[UserInfo]:
    response = await _post_request(url=url, json={"tid": telegram_id, "token": token})
    if response.status_code == code.NOT_FOUND:
        return None
    response.raise_for_status()
    user_info = await _parse_json_response_to_user_info(data=response.json())
    return user_info


async def _post_request(url, **kwargs) -> Response:
    async with AsyncClient() as client:
        response = await client.post(url=url, json=kwargs)
    response.raise_for_status()
    return response


async def _parse_json_response_to_user_info(data: dict) -> UserInfo:
    if not isinstance(data, dict):
        raise ValueError("Ответом должны быть словарь.")
    required_keys = [IS_APPROVED, FIRST_NAME, LAST_NAME, TARIFF]

    for key in required_keys:
        if key not in data:
            raise KeyError(f"В ответе нет ключа: {key}")

    tariff_value = data[TARIFF]
    if tariff_value not in ALL_TARIFFS:
        raise ValueError(
            f"Получено некорректное значение для тарифа: {tariff_value}."
            f" Ожидались: {ALL_TARIFFS}."
        )

    if not isinstance(data["isApproved"], bool):
        raise TypeError("isApproved должен соответствовать типу boolean.")
    if not isinstance(data["first_name"], str):
        raise TypeError("first_name должен соответствовать типу string.")
    if not isinstance(data["last_name"], str):
        raise TypeError("last_name должен соответствовать типу string.")

    return UserInfo(
        isApproved=data[IS_APPROVED],
        first_name=data[FIRST_NAME],
        last_name=data[LAST_NAME],
        tariff=tariff_value,
    )
