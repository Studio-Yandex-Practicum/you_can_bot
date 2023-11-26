import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", default="secret_key")
DEBUG = os.getenv("DEBUG", default=False)

ALLOWED_HOSTS = [os.getenv("ALLOWED_HOSTS", default="*")]
CSRF_TRUSTED_ORIGINS = (f"http://{os.getenv('HOST', default='127.0.0.1')}",)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "api.apps.ApiConfig",
    "info_pages.apps.InfoPagesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"
if os.getenv("NEED_SQLITE"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv(
                "DB_ENGINE",
                default="django.db.backends.postgresql_psycopg2",
            ),
            "NAME": os.getenv("POSTGRES_DB", default="postgres"),
            "USER": os.getenv("POSTGRES_USER", default="postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="postgres"),
            "HOST": os.getenv("DB_HOST", default="db"),
            "PORT": os.getenv("DB_PORT", default=5432),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
MAX_LENGTH_NAME = 150
MAX_LENGTH_SURNAME = 150

NOT_FOUND_QUESTION_ERROR_MESSAGE = "Не найден вопрос с таким номером."
NOT_FOUND_TASK_ERROR_MESSAGE = "Не найдено задание с таким номером."
NOT_FOUND_MENTOR_MESSAGE = "Не найдена учетная запись профдизайнера."

LOG_FILENAME = "backend.log"
LOG_PATH = BASE_DIR.parent / ".data" / os.getenv("LOG_DIR", "logs")
LOG_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH = LOG_PATH / LOG_FILENAME
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "[%(asctime)s,%(msecs)d] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
LOG_DT_FORMAT = "%d.%m.%y %H:%M:%S"

LOGGING = {
    "version": 1,
    "disable_exising_loggers": False,
    "formatters": {
        "general": {
            "format": LOG_FORMAT,
            "datefmt": LOG_DT_FORMAT,
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,
            "formatter": "general",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": LOG_PATH,
            "when": "midnight",
            "interval": 1,
            "backupCount": 14,
            "level": LOG_LEVEL,
            "formatter": "general",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
        },
        "api": {
            "handlers": ["console", "file"],
        },
    },
}

REST_FRAMEWORK = {
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

MAIN_MENTOR_ID = os.getenv(
    "MAIN_MENTOR_ID"
)  # id телеграма ментора, которому будут приходить вопросы, если пользователю еще не назначен ментор
