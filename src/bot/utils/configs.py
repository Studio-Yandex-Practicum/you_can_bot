import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE_PATH = LOG_DIR / 'tg_you_can.log'
LOG_FORMAT = "%(asctime)s - [%(levelname)s] - %(message)s"
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_BACKUP_COUNT = 5
LOG_MAX_SIZE = 50000000


def configure_logging() -> None:
    """
    Configure global logging.
    Logging into stdout and in log_file.
    """
    LOG_DIR.mkdir(exist_ok=True)
    rotating_handler = RotatingFileHandler(
        LOG_FILE_PATH, maxBytes=LOG_MAX_SIZE, backupCount=LOG_BACKUP_COUNT
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
