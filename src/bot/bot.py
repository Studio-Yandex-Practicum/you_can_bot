import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

load_dotenv()


def create_bot():
    """
    Create telegram bot application
    :return: Created telegram bot application
    """
    return ApplicationBuilder().token(os.getenv("TOKEN")).build()


def init_polling():
    """
    Initiate bot polling
    """
    bot_app = create_bot()
    bot_app.run_polling()
