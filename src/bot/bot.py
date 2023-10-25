from telegram.ext import ApplicationBuilder

from conversations.general.handlers import acquaintance_handler
from conversations.tasks.handlers import (
    task_one_handler,
    task_two_handler,
    task_three_handler,
    task_four_handler,
)
from utils.configs import TOKEN


def create_bot():
    """
    Create telegram bot application
    :return: Created telegram bot application
    """
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(handler=acquaintance_handler)
    bot_app.add_handler(handler=task_one_handler)
    bot_app.add_handler(handler=task_two_handler)
    bot_app.add_handler(handler=task_three_handler)
    bot_app.add_handler(handler=task_four_handler)

    return bot_app


def init_polling():
    """
    Initiate bot polling
    """
    bot_app = create_bot()
    bot_app.run_polling()
