import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

load_dotenv()


def create_bot():
    """
    Create telegram bot application
    :return: Created telegram bot application
    """
    bot_app = ApplicationBuilder().token(os.getenv("TOKEN")).build()
    return bot_app


def init_polling():
    """
    Initiate bot polling
    """
    bot_app = create_bot()
    bot_app.run_polling()
