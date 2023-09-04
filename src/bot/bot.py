from telegram.ext import ApplicationBuilder

from conversations.general.handlers import acquaintance_handler
from conversations.task_1.handlers import task_1_handler
from conversations.task_2.handlers import task_2_handler
from utils.configs import TOKEN


def create_bot():
    """
    Create telegram bot application
    :return: Created telegram bot application
    """
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(handler=acquaintance_handler)
    bot_app.add_handler(handler=task_1_handler)
    bot_app.add_handler(handler=task_2_handler)
    return bot_app


def init_polling():
    """
    Initiate bot polling
    """
    bot_app = create_bot()
    bot_app.run_polling()
