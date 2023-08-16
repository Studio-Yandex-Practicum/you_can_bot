from utils.logger import configure_logging
from bot import init_polling

if __name__ == "__main__":
    configure_logging()
    init_polling()
