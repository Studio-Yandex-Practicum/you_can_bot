from functools import wraps
from logging import DEBUG, getLogger
from typing import Optional, Union

from httpx import AsyncClient, HTTPStatusError, RequestError, codes

from utils.configs import TARIFFS, YOUCANBY_TOKEN, YOUCANBY_URL
from utils.logger import configure_logging

from .exceptions import APIForbiddenError, PostAPIError, UserNotFound

API_JSON_ERROR = '{key}: Отказ сервера {failure}.'
COMMON_ERROR = 'Сбой при получении ответа от сервера: {error}'
KEY_NOT_FOUND = 'Отсутствует ключ {key} в ключах ответа сервера.'
NETWORK_ERROR = 'Сбой сети {error} при запросе к {url} с телеграм id - {tid}'
STATUS_CODE_ERROR = (
    'Отказ сервера {status_code} при запросе к {url} с телеграм id - {tid}'
)
SUCCESS_RESPONSE = 'Запрос на {url} с телеграм id {tid} успешен.'
TARIFF_NOT_FOUND = 'Тариф {tariff} не соответствует ожидаемым {expected}.'
TELEGRAM_ID_NOT_INT = 'telegram_id должен быть числом.'
TELEGRAM_ID_NOT_POSITIVE = 'telegram_id должен быть положительным числом.'
TYPE_ERROR = 'В ответе сервера {type_response}, ожидалось {expected_type}.'
FIELDS_TYPE_ERROR = (
    'Для поля {key} ожидалось {expected_type}, в ответе сервера {type_response}.'
)
VARIABLE_ENV_NOT_FOUND = 'Не найдены переменные окружения: {tokens}.'
USER_NOT_FOUND = (
    '{status_code}: при запросе к {url} пользователь с id {tid} не найден.'
)

IS_APPROVED = 'isApproved'
FULL_NAME = 'full_name'
TARIFF = 'tariff'
USER_INFO_KEYS = (TARIFF, FULL_NAME, IS_APPROVED)

_LOGGER = getLogger(__name__)
configure_logging()
_LOGGER.setLevel(DEBUG)


def _check_telegram_id(telegram_id: int) -> None:
    """Проверяет корректность значения telegram_id.
    ### Args:
    - telegram_id (int):
        id пользователя в telegram
    ### Raises:
    - TypeError, ValueError
    ### Returns:
    - None
    """
    if not isinstance(telegram_id, int):
        raise TypeError(TELEGRAM_ID_NOT_INT)
    if telegram_id <= 0:
        raise ValueError(TELEGRAM_ID_NOT_POSITIVE)


def _logging_exceptions(func) -> dict[str, Union[str, bool]]:
    """Логгирование исключений запроса.
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
                NETWORK_ERROR.format(
                    error=error,
                    url=error.request.url,
                    **kwargs
                )
            )
        except HTTPStatusError as error:
            message = STATUS_CODE_ERROR.format(
                status_code=error.response.status_code,
                url=error.request.url,
                **kwargs
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
            raise HTTPStatusError(message)
        if response.status_code != codes.OK:
            raise PostAPIError(
                STATUS_CODE_ERROR.format(
                    status_code=response.status_code,
                    url=response.request.url,
                    **kwargs
                )
            )
        user_info = response.json()
        for key in ('error', 'code'):
            if key in user_info:
                raise PostAPIError(
                    API_JSON_ERROR.format(key=key, failure=user_info[key])
                )
        return user_info
    return wrapper


@_logging_exceptions
async def _post_request(**kwargs) -> dict[str, Union[str, bool]]:
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
    - KeyError, TypeError, ValueError
    ### Returns:
    - dict:
        {'tariff': str,
         'name': str,
         'surname': str,
         'is_approved': bool}
    """
    if not isinstance(data, dict):
        raise TypeError(
            TYPE_ERROR.format(type_response=type(data), expected_type=dict)
        )
    for key in USER_INFO_KEYS:
        if key not in data:
            raise KeyError(KEY_NOT_FOUND.format(key=key))
    tariff = data[TARIFF]
    if tariff not in TARIFFS:
        raise ValueError(
            TARIFF_NOT_FOUND.format(tariff=tariff, expected=TARIFFS)
        )
    full_name = data[FULL_NAME]
    if not isinstance(full_name, str):
        raise TypeError(
            TYPE_ERROR.format(
                type_response=type(full_name),
                expected_type=str
            )
        )
    name_surname = full_name.rsplit(' ', 1)
    if len(name_surname) == 2:
        name, surname = name_surname[0], name_surname[1]
    else:
        name, surname = full_name, ''
    is_apporved = data[IS_APPROVED]
    if not isinstance(is_apporved, bool):
        raise TypeError(
            TYPE_ERROR.format(
                type_response=type(is_apporved),
                expected_type=bool
            )
        )
    return {
        'tariff': tariff,
        'name': name,
        'surname': surname,
        'is_approved': is_apporved
    }


async def get_user_info_from_lk(telegram_id: int) -> Optional[dict]:
    """Получает данные о telegram-пользователе.
    ### Args:
    - telegram_id (int):
        id пользователя в telegram
    ### Raises:
    - APIForbiddenError, ConnectionError, HTTPStatusError,
      KeyError, PostAPIError, TypeError, UserNotFound,
      ValueError
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
