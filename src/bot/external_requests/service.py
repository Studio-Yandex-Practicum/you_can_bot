from logging import getLogger
from typing import Optional, TypedDict

from httpx import AsyncClient, Response, codes

from external_requests.exceptions import (
    TelegramIdError,
    UserNotFound,
    ValidationExternalResponseError,
)
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
    response = await _post_request(url=url, data={"tid": telegram_id, "token": token})
    if response.status_code == codes.NOT_FOUND:
        return None
    response.raise_for_status()
    user_info = await _parse_json_response_to_user_info(data=response.json())
    return user_info


async def _post_request(url, data) -> Response:
    async with AsyncClient() as client:
        response = await client.post(url=url, json=data)
    response.raise_for_status()
    return response


async def _parse_json_response_to_user_info(data: dict) -> UserInfo:
    if not isinstance(data, dict):
        raise ValidationExternalResponseError("Ответом должны быть словарь.")
    required_keys = [IS_APPROVED, FIRST_NAME, LAST_NAME, TARIFF]

    for key in required_keys:
        if key not in data:
            raise ValidationExternalResponseError(f"В ответе нет ключа: {key}")

    tariff_value = data[TARIFF]
    if tariff_value not in ALL_TARIFFS:
        raise ValidationExternalResponseError(
            f"Получено некорректное значение для тарифа: {tariff_value}."
            f" Ожидались: {ALL_TARIFFS}."
        )

    fields = {
        "isApproved": bool,
        "first_name": str,
        "last_name": str,
    }

    for field, expected_type in fields.items():
        if not isinstance(data.get(field), expected_type):
            raise ValidationExternalResponseError(
                f"{field} должен соответствовать типу {expected_type.__name__}. "
                f"Получен {type(data.get(field)).__name__}."
            )

    return UserInfo(
        isApproved=data[IS_APPROVED],
        first_name=data[FIRST_NAME],
        last_name=data[LAST_NAME],
        tariff=tariff_value,
    )
