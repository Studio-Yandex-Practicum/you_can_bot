from typing import Optional

from external_requests.service import (
    FIRST_NAME,
    IS_APPROVED,
    LAST_NAME,
    TARIFF,
    check_telegram_id,
)


async def get_user_info_from_lk(telegram_id: int) -> Optional[dict]:
    """Получает данные о telegram-пользователе."""
    check_telegram_id(telegram_id)
    return {
        TARIFF: "maxi",
        FIRST_NAME: "Павел",
        LAST_NAME: "Дуров",
        IS_APPROVED: True,
    }
