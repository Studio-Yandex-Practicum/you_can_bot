import unittest
from unittest.mock import AsyncMock, patch

from external_requests import service
from external_requests.exceptions import (
    UserNotFound,
    ValidationExternalResponseError,
)
from external_requests.service import (
    _normalize_tariff,
    _parse_json_response_to_user_info,
    get_user_info_from_lk,
)


def _user_info(tariff="maxi", first_name="Ann", last_name="Smith", is_approved=True):
    return {
        "isApproved": is_approved,
        "first_name": first_name,
        "last_name": last_name,
        "tariff": tariff,
    }


class NormalizeTariffTests(unittest.TestCase):
    def test_string_none_becomes_python_none(self):
        self.assertIsNone(_normalize_tariff("none"))

    def test_string_none_is_case_and_whitespace_insensitive(self):
        self.assertIsNone(_normalize_tariff("  NoNe "))

    def test_empty_string_becomes_python_none(self):
        self.assertIsNone(_normalize_tariff(""))

    def test_string_null_becomes_python_none(self):
        self.assertIsNone(_normalize_tariff("null"))

    def test_known_tariffs_are_unchanged(self):
        for tariff in ("mini", "midi", "maxi"):
            with self.subTest(tariff=tariff):
                self.assertEqual(_normalize_tariff(tariff), tariff)

    def test_python_none_is_unchanged(self):
        self.assertIsNone(_normalize_tariff(None))


class ParseJsonResponseTests(unittest.IsolatedAsyncioTestCase):
    async def test_tariff_string_none_is_accepted_and_normalized(self):
        data = _user_info(tariff="none", is_approved=False)

        result = await _parse_json_response_to_user_info(data)

        self.assertIsNone(result["tariff"])
        self.assertEqual(result["first_name"], "Ann")

    async def test_unknown_tariff_still_raises(self):
        data = _user_info(tariff="ultra")

        with self.assertRaises(ValidationExternalResponseError):
            await _parse_json_response_to_user_info(data)


class GetUserInfoFromLkTests(unittest.IsolatedAsyncioTestCase):
    async def test_robotguru_failure_does_not_drop_valid_youcanby_result(self):
        youcanby_result = _user_info(tariff="maxi")

        with patch.object(
            service,
            "_get_user_info_from_youcanby",
            new=AsyncMock(return_value=youcanby_result),
        ), patch.object(
            service,
            "_get_user_info_from_robotguru",
            new=AsyncMock(side_effect=ValidationExternalResponseError("boom")),
        ):
            result = await get_user_info_from_lk(123)

        self.assertEqual(result, youcanby_result)

    async def test_youcanby_failure_does_not_drop_valid_robotguru_result(self):
        robotguru_result = _user_info(tariff="midi", first_name="Bob")

        with patch.object(
            service,
            "_get_user_info_from_youcanby",
            new=AsyncMock(side_effect=ValidationExternalResponseError("boom")),
        ), patch.object(
            service,
            "_get_user_info_from_robotguru",
            new=AsyncMock(return_value=robotguru_result),
        ):
            result = await get_user_info_from_lk(123)

        self.assertEqual(result, robotguru_result)

    async def test_both_sources_return_none_raises_user_not_found(self):
        with patch.object(
            service,
            "_get_user_info_from_youcanby",
            new=AsyncMock(return_value=None),
        ), patch.object(
            service,
            "_get_user_info_from_robotguru",
            new=AsyncMock(return_value=None),
        ):
            with self.assertRaises(UserNotFound):
                await get_user_info_from_lk(123)

    async def test_both_sources_fail_reraises_first_error(self):
        youcanby_error = ValidationExternalResponseError("yc broken")

        with patch.object(
            service,
            "_get_user_info_from_youcanby",
            new=AsyncMock(side_effect=youcanby_error),
        ), patch.object(
            service,
            "_get_user_info_from_robotguru",
            new=AsyncMock(side_effect=ValidationExternalResponseError("rg broken")),
        ):
            with self.assertRaises(ValidationExternalResponseError) as ctx:
                await get_user_info_from_lk(123)

        self.assertIs(ctx.exception, youcanby_error)

    async def test_picks_higher_tariff_when_both_succeed(self):
        with patch.object(
            service,
            "_get_user_info_from_youcanby",
            new=AsyncMock(return_value=_user_info(tariff="mini")),
        ), patch.object(
            service,
            "_get_user_info_from_robotguru",
            new=AsyncMock(return_value=_user_info(tariff="maxi", first_name="Bob")),
        ):
            result = await get_user_info_from_lk(123)

        self.assertEqual(result["tariff"], "maxi")
        self.assertEqual(result["first_name"], "Bob")


if __name__ == "__main__":
    unittest.main()
