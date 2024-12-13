import logging
import os
from json import loads
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

ALLOWED_TARIFFS = loads(os.getenv("ALLOWED_TARIFFS", '["maxi"]'))
ALL_TARIFFS = loads(os.getenv("ALL_TARIFFS", '[null, "mini", "midi", "maxi"]'))
YOUCANBY_URL = os.getenv("YOUCANBY_URL")
YOUCANBY_TOKEN = os.getenv("YOUCANBY_TOKEN")
ROBOTGURU_URL = os.getenv("ROBOTGURU_URL")
ROBOTGURU_TOKEN = os.getenv("ROBOTGURU_TOKEN")
EXTERNAL_REQUESTS_ARE_MOCK = os.getenv("EXTERNAL_REQUESTS_ARE_MOCK") == "True"
MAIN_MENTOR_ID = os.getenv("MAIN_MENTOR_ID")

DEVELOPER_CHAT_ID = os.getenv("DEVELOPER_CHAT_ID", None)
