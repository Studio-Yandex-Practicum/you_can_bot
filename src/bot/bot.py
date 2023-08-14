from telegram.ext import ApplicationBuilder

from bot.utils.configs import TOKEN  # noqa


def create_bot():
    """
    Create telegram bot application
    :return: Created telegram bot application
    """
    bot_app = ApplicationBuilder().token(TOKEN).build()
    return bot_app


def init_polling():
    """
    Initiate bot polling
    """
    bot_app = create_bot()
    bot_app.run_polling()
