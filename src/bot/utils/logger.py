import logging
from logging.handlers import TimedRotatingFileHandler

from utils.configs import (
    LOG_BACKUP_COUNT,
    LOG_DIR,
    LOG_DT_FORMAT,
    LOG_ENCODING,
    LOG_FILE_PATH,
    LOG_FORMAT,
    LOG_INTERVAL,
    LOG_LEVEL,
    LOG_WHEN,
)


def configure_logging() -> None:
    """
    Configure global logging.
    Logging into stdout and in log_file.
    """
    LOG_DIR.mkdir(exist_ok=True)

    rotating_handler = TimedRotatingFileHandler(
        LOG_FILE_PATH,
        backupCount=LOG_BACKUP_COUNT,
        when=LOG_WHEN,
        interval=LOG_INTERVAL,
        encoding=LOG_ENCODING,
    )

    logging.basicConfig(
        datefmt=LOG_DT_FORMAT,
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        handlers=(rotating_handler, logging.StreamHandler()),
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
