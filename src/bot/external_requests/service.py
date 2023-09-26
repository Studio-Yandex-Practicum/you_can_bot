from functools import wraps
from logging import getLogger
from typing import Optional

from httpx import AsyncClient, HTTPStatusError, RequestError, Response, codes

from external_requests.exceptions import (
    APIDataError,
    APIForbiddenError,
    PostAPIError,
    TelegramIdError,
    UserNotFound
)
from utils.configs import TARIFFS, YOUCANBY_TOKEN, YOUCANBY_URL

API_JSON_ERROR = "{key}: Отказ сервера {failure}."
COMMON_ERROR = "Сбой при получении ответа от сервера: {error}"
KEY_NOT_FOUND = "Отсутствует ключ {key} в ключах ответа сервера."
NETWORK_ERROR = "Сбой сети {error} при запросе к {url} с телеграм id - {tid}"
STATUS_CODE_ERROR = (
    "Отказ сервера {status_code} при запросе к {url} с телеграм id - {tid}"
)
SUCCESS_RESPONSE = "Запрос на {url} с телеграм id {tid} успешен."
TARIFF_NOT_FOUND = "Тариф {tariff} не соответствует ожидаемым {expected}."
TELEGRAM_ID_NOT_INT = "telegram_id должен быть числом."
TELEGRAM_ID_NOT_POSITIVE = "telegram_id должен быть положительным числом."
TYPE_ERROR = "В ответе сервера {type_response}, ожидалось {expected_type}."
FIELDS_TYPE_ERROR = (
    "Для поля {key} ожидалось {expected_type}, в ответе сервера {type_response}."
)
VARIABLE_ENV_NOT_FOUND = "Не найдены переменные окружения: {tokens}."
USER_NOT_FOUND = "{status_code}: при запросе к {url} пользователь с id {tid} не найден."

IS_APPROVED = "isApproved"
FULL_NAME = "full_name"
TARIFF = "tariff"
USER_INFO_KEYS = (TARIFF, FULL_NAME, IS_APPROVED)

_LOGGER = getLogger(__name__)


async def get_user_info_from_lk(telegram_id: int) -> Optional[dict]:
    """Получает данные о telegram-пользователе.
    ### Args:
    - telegram_id (int):
        id пользователя в telegram
    ### Raises:
    - APIDataError, APIForbiddenError, ConnectionError, HTTPStatusError,
      PostAPIError, TelegramIdError, UserNotFound
    ### Returns:
    - Optional[dict]:
        {'tariff': str,
         'name': str,
         'surname': str,
         'is_approved': bool}
    """
    _check_telegram_id(telegram_id)
    try:
        user_info = await _post_request(tid=telegram_id, token=YOUCANBY_TOKEN)
        parsed_info = await _parse_data(user_info)
    except APIForbiddenError as exception:
        _LOGGER.critical(COMMON_ERROR.format(error=exception))
        raise exception
    except UserNotFound as exception:
        _LOGGER.debug(COMMON_ERROR.format(error=exception))
        raise exception
    except Exception as exception:
        _LOGGER.error(COMMON_ERROR.format(error=exception))
        raise exception
    _LOGGER.debug(SUCCESS_RESPONSE.format(tid=telegram_id, url=YOUCANBY_URL))
    return parsed_info


def _check_telegram_id(telegram_id: int) -> None:
    """Проверяет корректность значения telegram_id.
    ### Args:
    - telegram_id (int):
        id пользователя в telegram
    ### Raises:
    - TelegramIdError
    ### Returns:
    - None
    """
    if not isinstance(telegram_id, int):
        raise TelegramIdError(TELEGRAM_ID_NOT_INT)
    if telegram_id <= 0:
        raise TelegramIdError(TELEGRAM_ID_NOT_POSITIVE)


def _logging_exceptions(func):
    """Логирование исключений запроса.
    ### Args:
    - func (function):
        функция отправляющая запрос
    ### Raises:
    - APIForbiddenError, ConnectionError, HTTPStatusError,
      PostAPIError, UserNotFound
    ### Returns:
    - dict[str, Union[str, bool]]
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            response = await func(*args, **kwargs)
            response.raise_for_status()
        except RequestError as error:
            raise ConnectionError(
                NETWORK_ERROR.format(error=error, url=error.request.url, **kwargs)
            )
        except HTTPStatusError as error:
            message = STATUS_CODE_ERROR.format(
                status_code=error.response.status_code, url=error.request.url, **kwargs
            )
            if error.response.status_code == codes.FORBIDDEN:
                raise APIForbiddenError(message)
            if error.response.status_code == codes.NOT_FOUND:
                raise UserNotFound(
                    USER_NOT_FOUND.format(
                        status_code=error.response.status_code,
                        url=error.request.url,
                        **kwargs
                    )
                )
            raise HTTPStatusError(
                message, request=error.request, response=error.response
            )
        if response.status_code != codes.OK:
            raise PostAPIError(
                STATUS_CODE_ERROR.format(
                    status_code=response.status_code, url=response.request.url, **kwargs
                )
            )
        user_info = response.json()
        for key in ("error", "code"):
            if key in user_info:
                raise PostAPIError(
                    API_JSON_ERROR.format(key=key, failure=user_info[key])
                )
        return user_info

    return wrapper


@_logging_exceptions
async def _post_request(**kwargs) -> Response:
    """Отправляет post-запрос.
    ### Kwargs:
    - именованные аргументы для json
    ### Raises:
    - APIForbiddenError, ConnectionError, HTTPStatusError,
      PostAPIError, UserNotFound
    ### Returns:
    - dict[str, Union[str, bool]]
    """
    async with AsyncClient() as client:
        response = await client.post(url=YOUCANBY_URL, json=kwargs)
    return response


async def _parse_data(data: dict) -> dict[str, str]:
    """Обрабатывает полученные данные.
    Возвращает словарь с данными пользователя.
    ### Args:
    - response (dict):
        ответ сервера
    ### Raises:
    - APIDataError
    ### Returns:
    - dict:
        {'tariff': str,
         'name': str,
         'surname': str,
         'is_approved': bool}
    """
    DATA_TYPE = dict
    IS_APPROVED_TYPE = bool
    FULL_NAME_TYPE = str
    if not isinstance(data, DATA_TYPE):
        raise APIDataError(
            TYPE_ERROR.format(type_response=type(data), expected_type=DATA_TYPE)
        )
    for key in USER_INFO_KEYS:
        if key not in data:
            raise APIDataError(KEY_NOT_FOUND.format(key=key))
    tariff = data[TARIFF]
    if tariff not in TARIFFS:
        raise APIDataError(TARIFF_NOT_FOUND.format(tariff=tariff, expected=TARIFFS))
    full_name = data[FULL_NAME]
    if not isinstance(full_name, FULL_NAME_TYPE):
        raise APIDataError(
            TYPE_ERROR.format(
                type_response=type(full_name),
                expected_type=FULL_NAME_TYPE
            )
        )
    name_surname = full_name.rsplit(" ", 1)
    if len(name_surname) == 2:
        name, surname = name_surname[0], name_surname[1]
    else:
        name, surname = full_name, ""
    is_approved = data[IS_APPROVED]
    if not isinstance(is_approved, IS_APPROVED_TYPE):
        raise APIDataError(
            TYPE_ERROR.format(
                type_response=type(is_approved),
                expected_type=IS_APPROVED_TYPE
            )
        )
    return {
        "tariff": tariff,
        "name": name,
        "surname": surname,
        "is_approved": is_approved,
    }
