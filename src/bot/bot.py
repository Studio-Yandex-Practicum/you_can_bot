from telegram.ext import Application, ApplicationBuilder

from conversations.general.handlers import acquaintance_handler
from conversations.mentor_registration.handlers import (
    mentor_registration_handler,
    registration_confirmation_handler,
)
from conversations.menu.handlers import (
    ask_question_handler,
    entry_point_to_ask_handler,
    entry_point_to_tasks_handler,
    info_handler,
    show_all_tasks_handler,
)
from conversations.menu.keyboards import get_main_menu_commands
from conversations.task_1.handlers import task_one_handler
from conversations.task_2.handlers import task_two_handler
from conversations.task_3.handlers import task_three_handler
from conversations.task_4.handlers import task_four_handler
from conversations.task_5.handlers import task_five_handler
from conversations.task_6.handlers import task_six_handler
from conversations.task_7.handlers import task_seven_handler
from conversations.task_8.handlers import task_8_handler
from utils.configs import TOKEN


async def post_init(application: Application) -> None:
    """Создает кнопку меню и наполняет ее командами."""
    await application.bot.set_my_commands(get_main_menu_commands())


def create_bot():
    """
    Create telegram bot application
    :return: Created telegram bot application
    """
    bot_app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    bot_app.add_handler(handler=acquaintance_handler)

    # task handlers
    bot_app.add_handlers(
        handlers=[
            task_one_handler,
            task_two_handler,
            task_three_handler,
            task_four_handler,
            task_five_handler,
            task_six_handler,
            task_seven_handler,
            task_8_handler,
        ],
        group=2,
    )

    # mentor registration handlers
    bot_app.add_handler(handler=mentor_registration_handler)
    bot_app.add_handler(handler=registration_confirmation_handler)

    # menu handlers
    bot_app.add_handler(handler=ask_question_handler)
    bot_app.add_handler(handler=show_all_tasks_handler)
    bot_app.add_handler(handler=info_handler)
    bot_app.add_handlers(
        handlers=[
            entry_point_to_tasks_handler,
            entry_point_to_ask_handler,
        ]
    )

    return bot_app


def init_polling():
    """
    Initiate bot polling
    """
    bot_app = create_bot()
    bot_app.run_polling()
