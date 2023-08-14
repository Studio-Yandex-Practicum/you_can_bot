import os
import asyncio

from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import ApplicationBuilder

from .conversations.menu.keyboards import create_main_menu


load_dotenv()


def create_bot():
    """
    Create telegram bot application
    :return: Created telegram bot application
    """
    bot_app = ApplicationBuilder().token(os.getenv("TOKEN")).build()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_main_menu(Bot(os.getenv("TOKEN"))))
    return bot_app


def init_polling():
    """
    Initiate bot polling
    """
    bot_app = create_bot()
    bot_app.run_polling()
