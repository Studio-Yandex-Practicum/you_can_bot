from unittest import IsolatedAsyncioTestCase


class CaseForGetUserInfoFromLK(IsolatedAsyncioTestCase):

    ERROR_JSON = {'code': 'test_error'}
    FAKE_URL = 'https://api.test_endpoint'
    JSON_TARIFF_MINI = {
        'tariff': 'mini', 'full_name': 'Егор Иванов', 'isApproved': True
    }
    JSON_TARIFF_MIDI = {
        'tariff': 'midi', 'full_name': 'Егор Иванов', 'isApproved': True
    }
    JSON_TARIFF_MAXI = {
        'tariff': 'maxi', 'full_name': 'Егор Иванов', 'isApproved': True
    }
    JSON_TARIFF_NONE = {
        'tariff': None, 'full_name': 'Егор Иванов', 'isApproved': True
    }
    JSON_UNEXPECTED_TYPE_TARIFF = {
        'tariff': 'Mini', 'full_name': 'Егор Иванов', 'isApproved': True
    }
    JSON_UNEXPECTED_TYPE_FULL_NAME = {
        'tariff': 'mini', 'full_name': ('Егор', 'Иванов'), 'isApproved': True
    }
    JSON_UNEXPECTED_TYPE_ISAPPROVED = {
        'tariff': 'mini', 'full_name': 'Егор Иванов', 'isApproved': 'true'
    }
    JSON_WITH_DOUBLE_SPACE_IN_NAME = {
        'tariff': 'mini', 'full_name': 'Егор Денисович Иванов', 'isApproved': True
    }
    JSON_WITHOUT_TARIFF = {'full_name': 'Егор Иванов', 'isApproved': True}
    JSON_WITHOUT_FULL_NAME = {'tariff': 'mini', 'isApproved': True}
    JSON_WITHOUT_SURNAME = {
        'tariff': 'mini', 'full_name': 'Егор', 'isApproved': True
    }
    JSON_WITHOUT_ISAPPROVED = {'tariff': 'mini', 'full_name': 'Егор Иванов'}
    MESSAGE_403_FORBIDDEN = 'test_403_Forbidden'
    MESSAGE_404_NOT_FOUND = 'test_404_Not_Found'
    MESSAGE_REQUEST_ERROR = 'test_RequestError'
    NEGATIVE_INT = -2
    RETURN_WITH_DOUBLE_SPACE_IN_NAME = {
        'tariff': 'mini', 'name': 'Егор Денисович',
        'surname': 'Иванов', 'is_approved': True
    }
    RETURN_WITHOUT_SURNAME = {
        'tariff': 'mini', 'name': 'Егор',
        'surname': '', 'is_approved': True
    }
    TELEGRAM_ID = 2
    STRING = 'string'
    SUCCESS_JSON = {
        'tariff': 'mini', 'full_name': 'Егор Иванов', 'isApproved': True
    }
    SUCCESS_USER_INFO = {'tariff': 'mini', 'name': 'Егор',
                         'surname': 'Иванов', 'is_approved': True}
    UNEXPECTED_STATUS_CODE = 333
