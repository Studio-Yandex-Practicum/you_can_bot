from telegram.ext import Application, ApplicationBuilder

from conversations.general.handlers import acquaintance_handler
from conversations.menu.handlers import (
    ask_question_handler,
    info_handler,
    profile_handler,
    show_all_tasks_handler,
    show_user_results_handler,
)
from conversations.menu.keyboards import get_main_menu_commands
from conversations.task_1.handlers import task_1_handler
from conversations.task_2.handlers import task_2_handler
from conversations.task_3.handlers import task_3_handler
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
    bot_app.add_handler(handler=task_1_handler)
    bot_app.add_handler(handler=task_2_handler)
    bot_app.add_handler(handler=task_3_handler)

    # menu handlers
    bot_app.add_handler(handler=profile_handler)
    bot_app.add_handler(handler=ask_question_handler)
    bot_app.add_handlers(
        handlers=[
            show_all_tasks_handler,
            show_user_results_handler,
            info_handler,
        ]
    )

    return bot_app


def init_polling():
    """
    Initiate bot polling
    """
    bot_app = create_bot()
    bot_app.run_polling()
