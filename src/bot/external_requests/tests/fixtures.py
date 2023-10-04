from unittest import IsolatedAsyncioTestCase


class CaseForGetUserInfoFromLK(IsolatedAsyncioTestCase):
    DOUBLE_SPACE_IN_NAME = {
        "tariff": "mini",
        "full_name": "Егор Денисович Иванов",
        "isApproved": True,
    }
    ERROR_CODE = {"code": "test_error"}
    FAKE_URL = "https://api.test_endpoint"
    MESSAGE_403_FORBIDDEN = "test_403_Forbidden"
    MESSAGE_404_NOT_FOUND = "test_404_Not_Found"
    MESSAGE_REQUEST_ERROR = "test_RequestError"
    NEGATIVE_NUMBER = -2
    NO_FULL_NAME = {"tariff": "mini", "isApproved": True}
    NO_IS_APPROVED = {"tariff": "mini", "full_name": "Егор Иванов"}
    NO_SURNAME = {"tariff": "mini", "full_name": "Егор", "isApproved": True}
    NO_TARIFF = {"full_name": "Егор Иванов", "isApproved": True}
    RETURN_DOUBLE_SPACE_IN_NAME = {
        "tariff": "mini",
        "name": "Егор Денисович",
        "surname": "Иванов",
        "is_approved": True,
    }
    RETURN_NO_SURNAME = {
        "tariff": "mini",
        "name": "Егор",
        "surname": "",
        "is_approved": True,
    }
    STRING = "string"
    SUCCESS_DATA = {"tariff": "mini", "full_name": "Егор Иванов", "isApproved": True}
    SUCCESS_USER_INFO = {
        "tariff": "mini",
        "name": "Егор",
        "surname": "Иванов",
        "is_approved": True,
    }
    TARIFF_MINI = {"tariff": "mini", "full_name": "Егор Иванов", "isApproved": True}
    TARIFF_MIDI = {"tariff": "midi", "full_name": "Егор Иванов", "isApproved": True}
    TARIFF_MAXI = {"tariff": "maxi", "full_name": "Егор Иванов", "isApproved": True}
    TARIFF_NONE = {"tariff": None, "full_name": "Егор Иванов", "isApproved": True}
    TELEGRAM_ID = 2
    UNEXPECTED_STATUS_CODE = 333
    UNEXPECTED_TYPE_TARIFF = {
        "tariff": "Mini",
        "full_name": "Егор Иванов",
        "isApproved": True,
    }
    UNEXPECTED_TYPE_FULL_NAME = {
        "tariff": "mini",
        "full_name": ("Егор", "Иванов"),
        "isApproved": True,
    }
    UNEXPECTED_TYPE_ISAPPROVED = {
        "tariff": "mini",
        "full_name": "Егор Иванов",
        "isApproved": "true",
    }
