from unittest import IsolatedAsyncioTestCase

FULL_NAME_KEY = "full_name"
IS_APPROVED_EXTERNAL_KEY = "isApproved"

NAME_KEY = "name"
SURNAME_KEY = "surname"
IS_APPROVED_INTERNAL_KEY = "is_approved"
TARIFF_KEY = "tariff"

MINI_TARIFF = "mini"
MIDI_TARIFF = "midi"
MAXI_TARIFF = "maxi"

TEST_NAME = "Иван"
TEST_SURNAME = "Иванов"
TEST_FULLNAME = f"{TEST_SURNAME} {TEST_NAME}"


class CaseForGetUserInfoFromLK(IsolatedAsyncioTestCase):
    DOUBLE_SPACE_IN_NAME = {
        TARIFF_KEY: MINI_TARIFF,
        FULL_NAME_KEY: f"{TEST_SURNAME} {TEST_NAME} Иванович",
        IS_APPROVED_EXTERNAL_KEY: True,
    }
    ERROR_CODE = {"code": "test_error"}
    FAKE_URL = "https://api.test_endpoint"
    MESSAGE_403_FORBIDDEN = "test_403_Forbidden"
    MESSAGE_404_NOT_FOUND = "test_404_Not_Found"
    MESSAGE_REQUEST_ERROR = "test_RequestError"
    NEGATIVE_NUMBER = -2
    NO_FULL_NAME = {TARIFF_KEY: MINI_TARIFF, IS_APPROVED_EXTERNAL_KEY: True}
    NO_IS_APPROVED = {TARIFF_KEY: MINI_TARIFF, FULL_NAME_KEY: TEST_FULLNAME}
    NO_SURNAME = {
        TARIFF_KEY: MINI_TARIFF,
        FULL_NAME_KEY: TEST_NAME,
        IS_APPROVED_EXTERNAL_KEY: True,
    }
    NO_TARIFF = {FULL_NAME_KEY: TEST_FULLNAME, IS_APPROVED_EXTERNAL_KEY: True}
    RETURN_DOUBLE_SPACE_IN_NAME = {
        TARIFF_KEY: MINI_TARIFF,
        NAME_KEY: TEST_NAME,
        SURNAME_KEY: TEST_SURNAME,
        IS_APPROVED_INTERNAL_KEY: True,
    }
    RETURN_NO_SURNAME = {
        TARIFF_KEY: MINI_TARIFF,
        NAME_KEY: TEST_NAME,
        SURNAME_KEY: "",
        IS_APPROVED_INTERNAL_KEY: True,
    }
    STRING = "string"
    SUCCESS_DATA = {
        TARIFF_KEY: MINI_TARIFF,
        FULL_NAME_KEY: TEST_FULLNAME,
        IS_APPROVED_EXTERNAL_KEY: True,
    }
    SUCCESS_USER_INFO = {
        TARIFF_KEY: MINI_TARIFF,
        NAME_KEY: TEST_NAME,
        SURNAME_KEY: TEST_SURNAME,
        IS_APPROVED_INTERNAL_KEY: True,
    }
    TARIFF_MINI = {
        TARIFF_KEY: MINI_TARIFF,
        FULL_NAME_KEY: TEST_FULLNAME,
        IS_APPROVED_EXTERNAL_KEY: True,
    }
    TARIFF_MIDI = {
        TARIFF_KEY: MIDI_TARIFF,
        FULL_NAME_KEY: TEST_FULLNAME,
        IS_APPROVED_EXTERNAL_KEY: True,
    }
    TARIFF_MAXI = {
        TARIFF_KEY: MAXI_TARIFF,
        FULL_NAME_KEY: TEST_FULLNAME,
        IS_APPROVED_EXTERNAL_KEY: True,
    }
    TARIFF_NONE = {
        TARIFF_KEY: None,
        FULL_NAME_KEY: TEST_FULLNAME,
        IS_APPROVED_EXTERNAL_KEY: True,
    }
    TELEGRAM_ID = 2
    UNEXPECTED_STATUS_CODE = 333
    UNEXPECTED_TYPE_TARIFF = {
        TARIFF_KEY: "Mini",
        FULL_NAME_KEY: TEST_FULLNAME,
        IS_APPROVED_EXTERNAL_KEY: True,
    }
    UNEXPECTED_TYPE_FULL_NAME = {
        TARIFF_KEY: MINI_TARIFF,
        FULL_NAME_KEY: (TEST_NAME, TEST_SURNAME),
        IS_APPROVED_EXTERNAL_KEY: True,
    }
    UNEXPECTED_TYPE_ISAPPROVED = {
        TARIFF_KEY: MINI_TARIFF,
        FULL_NAME_KEY: TEST_FULLNAME,
        IS_APPROVED_EXTERNAL_KEY: "true",
    }
