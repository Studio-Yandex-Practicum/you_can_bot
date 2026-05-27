import logging

from telegram.constants import ParseMode
from telegram.ext import (
    AIORateLimiter,
    Application,
    ApplicationBuilder,
    Defaults,
    PicklePersistence,
)

from conversations.general.handlers import acquaintance_handler
from conversations.mentor_registration.handlers import (
    mentor_registration_handler,
    registration_confirmation_handler,
)
from conversations.menu.cancel_command.handlers import no_active_dialog_cancel_handler
from conversations.menu.handlers import (
    ask_question_handler,
    info_handler,
    show_all_tasks_handler,
)
from conversations.menu.keyboards import get_main_menu_commands
from conversations.task_1.handlers import task_one_conv
from conversations.task_2.handlers import task_two_conv
from conversations.task_3.handlers import task_three_conv
from conversations.task_4.handlers import task_four_conv
from conversations.task_5.handlers import task_five_conv
from conversations.task_6.handlers import task_six_conv
from conversations.task_7.handlers import task_seven_conv
from conversations.task_8.handlers import task_8_conv
from utils.configs import (
    PERSISTENCE_DIR,
    PERSISTENCE_FILE_PATH,
    SOCKS5_PROXY_URL,
    TOKEN,
)
from utils.telegram_retry import RetryingHTTPXRequest


async def post_init(application: Application) -> None:
    """Создает кнопку меню и наполняет ее командами."""
    await application.bot.set_my_commands(get_main_menu_commands())


_LOGGER = logging.getLogger(__name__)


def create_bot():
    """
    Create telegram bot application
    :return: Created telegram bot application
    """
    defaults = Defaults(parse_mode=ParseMode.HTML)

    PERSISTENCE_DIR.mkdir(parents=True, exist_ok=True)
    builder = (
        ApplicationBuilder()
        .token(TOKEN)
        .defaults(defaults)
        .rate_limiter(AIORateLimiter(max_retries=3))
        .persistence(PicklePersistence(filepath=PERSISTENCE_FILE_PATH))
        .post_init(post_init)
    )
    builder = builder.request(
        RetryingHTTPXRequest(proxy=SOCKS5_PROXY_URL or None, connection_pool_size=256)
    ).get_updates_request(RetryingHTTPXRequest(proxy=SOCKS5_PROXY_URL or None))
    bot_app = builder.build()

    # mentor registration handlers
    bot_app.add_handler(handler=mentor_registration_handler)
    bot_app.add_handler(handler=registration_confirmation_handler)

    # menu handlers
    bot_app.add_handler(handler=acquaintance_handler)
    bot_app.add_handler(handler=ask_question_handler)
    bot_app.add_handler(handler=show_all_tasks_handler)
    bot_app.add_handler(handler=info_handler)

    # tasks
    bot_app.add_handlers(
        handlers=[
            task_one_conv,
            task_two_conv,
            task_three_conv,
            task_four_conv,
            task_five_conv,
            task_six_conv,
            task_seven_conv,
            task_8_conv,
        ]
    )

    bot_app.add_handler(no_active_dialog_cancel_handler)

    return bot_app


def init_polling():
    """
    Initiate bot polling
    """
    bot_app = create_bot()
    bot_app.run_polling()
