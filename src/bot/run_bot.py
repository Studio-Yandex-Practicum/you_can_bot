from bot import init_polling
from utils.logger import configure_logging
from utils.monitoring import configure_monitoring

if __name__ == "__main__":
    configure_logging()
    configure_monitoring()
    init_polling()
