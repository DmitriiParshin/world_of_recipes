import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = BASE_DIR / ".env"
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-rms07%07)yyw7doud#^8m_y@%xt%a^(#_z5x3&%(flin3yfv(!",
)

DEBUG = int(os.getenv("DEBUG", 0))

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "158.160.9.121 localhost 127.0.0.1 backend foodgram29.hopto.org",
).split(" ")

CORS_ALLOWED_ORIGINS = [
    "http://*localhost",
    "https://*localhost",
    "http://*foodgram29.hopto.org",
    "https://*foodgram29.hopto.org",
    "http://127.0.0.1",
    "https://127.0.0.1",
]
CORS_URLS_REGEXES = [r"^/api/.*$", r"^/admin/.*$", r"^/swagger/.*$"]

CSRF_TRUSTED_ORIGINS = [
    "http://*localhost",
    "https://*localhost",
    "http://*foodgram29.hopto.org",
    "https://*foodgram29.hopto.org",
    "http://127.0.0.1",
    "https://127.0.0.1",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "corsheaders",
    "api.apps.ApiConfig",
    "recipes.apps.RecipesConfig",
    "users.apps.UsersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "app.wsgi.application"

DB_TYPE = os.getenv("DB_TYPE", "postgres")
if DB_TYPE == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
            "NAME": os.getenv("DB_NAME", "postgres"),
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
            "HOST": os.getenv("DB_HOST", "localhost"),
            "PORT": os.getenv("DB_PORT", 5432),
        }
    }
elif DB_TYPE == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    raise ValueError("Unknown database type")

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

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Kaliningrad"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 6,
    "SEARCH_PARAM": "name",
}

DJOSER = {
    "LOGIN_FIELD": "email",
    "SEND_ACTIVATION_EMAIL": False,
    "HIDE_USERS": False,
    "SERIALIZERS": {
        "user": "api.serializers.CustomUserSerializer",
        "current_user": "api.serializers.CustomUserSerializer",
    },
    "PERMISSIONS": {
        "user": ["djoser.permissions.CurrentUserOrAdminOrReadOnly"],
        "user_list": ["rest_framework.permissions.AllowAny"],
    },
}

AUTH_USER_MODEL = "users.CustomUser"

OUTPUT_LENGTH = 50

LIMIT_USERNAME = 150

LIMIT_EMAIL = 254

LIMIT_COLOR = 7

LIMIT_NAME = 200

MIN_VALUE = 1
