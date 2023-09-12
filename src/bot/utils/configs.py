import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

TOKEN = os.getenv("TOKEN")

BASE_DIR = Path(__file__).parent.parent

LOG_DIR = BASE_DIR.parent / ".data" / os.getenv("LOG_DIR", default="logs")
LOG_FILE_PATH = LOG_DIR / "bot.log"
LOG_LEVEL = LOG_LEVELS.get(os.getenv("LOG_LEVEL", default="INFO"), logging.INFO)

LOG_FORMAT = "[%(asctime)s,%(msecs)d] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
LOG_DT_FORMAT = "%d.%m.%y %H:%M:%S"

LOG_WHEN = "midnight"
LOG_INTERVAL = 1
LOG_BACKUP_COUNT = 14
LOG_ENCODING = "UTF-8"

INTERNAL_API_URL = "api/v1"
