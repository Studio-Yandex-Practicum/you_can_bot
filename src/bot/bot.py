import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from conversations.general.handlers import acquaintance_handler

load_dotenv()


def create_bot():
    """
    Create telegram bot application
    :return: Created telegram bot application
    """
    bot_app = ApplicationBuilder().token(os.getenv("TOKEN")).build()
    bot_app.add_handlers((acquaintance_handler,))
    return bot_app


def init_polling():
    """
    Initiate bot polling
    """
    bot_app = create_bot()
    bot_app.run_polling()
