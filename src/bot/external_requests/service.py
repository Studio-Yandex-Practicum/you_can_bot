import logging
from typing import Optional, Union

from httpx import AsyncClient, codes, HTTPStatusError, RequestError

from .exceptions import APIForbiddenError, PostAPIError, UserNotFound
from utils.configs import YOUCANBY_TOKEN, YOUCANBY_URL
from utils.logger import configure_logging

API_JSON_ERROR = '{key}: Отказ сервера {failure} на запрос к {url}.'
COMMON_ERROR = 'Сбой при получении ответа от сервера: {error}'
KEY_NOT_FOUND = 'Отсутствует ключ {key} в ключах ответа сервера.'
NETWORK_ERROR = 'Сбой сети {error} при запросе к {url} с телеграм id - {tid}'
STATUS_CODE_ERROR = (
    'Отказ сервера {status_code} при запросе к {url} с телеграм id - {tid}'
)
SUCCESS_RESPONSE = 'Запрос на {url} с телеграм id {tid} успешен.'
TARIFFS_NOT_FOUND = 'Тариф {tariff} не соответствует ожидаемым {expected}.'
TELEGRAM_ID_NOT_INT = 'telegram_id должен быть числом.'
TELEGRAM_ID_NOT_POSITIVE = 'telegram_id должен быть положительным числом.'
TYPE_ERROR = 'В ответе сервера {type_response}, ожидалось {expected}.'
VARIABLE_ENV_NOT_FOUND = 'Не найдены переменные окружения: {tokens}.'
USER_NOT_FOUND = (
    '{status_code}: при запросе к {url} пользователь с id {tid} не найден.'
)

ENV_NAMES = ('YOUCANBY_URL', 'YOUCANBY_TOKEN')
TARIFFS = ('mini', 'midi', 'maxi', None)
USER_INFO = ('tariff', 'full_name', 'isApproved')

_LOGGER = logging.getLogger(__name__)
configure_logging()
_LOGGER.setLevel(logging.DEBUG)


def _check_telegram_id(telegram_id: int) -> None:
    """Проверяет доступность переменных окружения.
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


async def _post_request(data: dict) -> dict[str, Union[str, bool]]:
    """Отправляет post-запрос.
    ### Args:
    - data (dict):
        данные запроса
    ### Raises:
    - APIForbiddenError, ConnectionError, HTTPStatusError,
      PostAPIError, UserNotFound
    ### Returns:
    - dict[str, Union[str, bool]]
    """
    try:
        async with AsyncClient() as client:
            response = await client.post(url=YOUCANBY_URL, json=data)
    except RequestError as error:
        raise ConnectionError(
            NETWORK_ERROR.format(
                error=error,
                url=error.request.url,
                **data
            )
        )
    except HTTPStatusError as error:
        message = STATUS_CODE_ERROR.format(
            status_code=error.response.status_code,
            url=error.request.url,
            **data
        )
        if error.response.status_code == codes.FORBIDDEN:
            raise APIForbiddenError(message)
        if error.response.status_code == codes.NOT_FOUND:
            raise UserNotFound(
                USER_NOT_FOUND.format(
                    status_code=error.response.status_code,
                    url=error.request.url,
                    **data)
            )
        raise HTTPStatusError(message)
    if response.status_code != codes.OK:
        raise PostAPIError(
            STATUS_CODE_ERROR.format(
                status_code=response.status_code,
                url=response.request.url,
                **data
            )
        )
    user_info = response.json()
    for key in ('error', 'code'):
        if key in user_info:
            raise PostAPIError(
                API_JSON_ERROR.format(
                    key=key,
                    failure=user_info[key],
                    **data
                )
            )
    return user_info


async def _parse_data(data: dict) -> dict[str, str]:
    """Получает строку с именем и фамилией.
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
            TYPE_ERROR.format(type_response=type(data), expected=dict)
        )
    for key in USER_INFO:
        if key not in data:
            raise KeyError(KEY_NOT_FOUND.format(key=key))
    tariff = data['tariff']
    if tariff not in TARIFFS:
        raise ValueError(
            TARIFFS_NOT_FOUND.format(tariff=tariff, excepted=TARIFFS)
        )
    full_name = data['full_name']
    if not isinstance(full_name, str):
        raise TypeError(
            TYPE_ERROR.format(
                type_response=type(full_name),
                excepted_type=str
            )
        )
    name_surname = full_name.rsplit(' ', 1)
    if len(name_surname) == 2:
        name, surname = name_surname[0], name_surname[1]
    else:
        name, surname = full_name, ''
    is_apporved = data['isApproved']
    if not isinstance(is_apporved, bool):
        raise TypeError(
            TYPE_ERROR.format(
                type_response=type(is_apporved),
                excepted_type=bool
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
    - TypeError, ValueError
    ### Returns:
    - Optional[dict]:
        {'tariff': str,
         'name': str,
         'surname': str,
         'is_approved': bool}
    """
    _check_telegram_id(telegram_id)
    try:
        user_info = await _post_request({'tid': telegram_id, 'token': YOUCANBY_TOKEN})
        parsed_info = await _parse_data(user_info)
    except APIForbiddenError as error:
        _LOGGER.critical(COMMON_ERROR.format(error=error))
    except UserNotFound as exception:
        _LOGGER.debug(COMMON_ERROR.format(error=exception))
    except Exception as error:
        _LOGGER.error(COMMON_ERROR.format(error=error))
    else:
        _LOGGER.debug(SUCCESS_RESPONSE.format(url=YOUCANBY_URL, tid=telegram_id))
        return parsed_info
