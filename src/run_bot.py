from bot.bot import init_polling
from bot.utils.configs import configure_logging

if __name__ == "__main__":
    configure_logging()
    init_polling()
