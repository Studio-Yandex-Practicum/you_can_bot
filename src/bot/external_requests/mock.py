from typing import Optional

from external_requests import IS_APPROVED, NAME, SURNAME, TARIFF
from external_requests.service import check_telegram_id


async def get_user_info_from_lk(telegram_id: int) -> Optional[dict]:
    """Получает данные о telegram-пользователе."""
    check_telegram_id(telegram_id)
    return {
        TARIFF: "midi",
        NAME: "Павел",
        SURNAME: "Дуров",
        IS_APPROVED: True,
    }
