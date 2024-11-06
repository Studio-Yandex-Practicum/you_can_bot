from utils.configs import EXTERNAL_REQUESTS_ARE_MOCK

if EXTERNAL_REQUESTS_ARE_MOCK is True:
    from .mock import get_user_info_from_lk  # noqa
else:
    from .service import get_user_info_from_lk  # noqa
