import os

from dotenv import load_dotenv
from telegram.ext import Application

from .conversations.menu.keyboards import get_main_menu_commands
from .conversations.menu.handlers import (
    profile_handler, ask_question_handler, show_all_tasks_handler,
    show_user_results_handler, info_handler)


load_dotenv()


async def post_init(application: Application) -> None:
    "Создает кнопку меню и наполняет ее командами."
    await application.bot.set_my_commands(get_main_menu_commands())


def create_bot():
    """
    Create telegram bot application
    :return: Created telegram bot application
    """
    bot_app = Application.builder().token(os.getenv("TOKEN")).post_init(post_init).build()
    bot_app.add_handler(profile_handler)
    bot_app.add_handler(ask_question_handler)
    bot_app.add_handler(show_all_tasks_handler)
    bot_app.add_handler(show_user_results_handler)
    bot_app.add_handler(info_handler)
    return bot_app


def init_polling():
    """
    Initiate bot polling
    """
    bot_app = create_bot()
    bot_app.run_polling()
