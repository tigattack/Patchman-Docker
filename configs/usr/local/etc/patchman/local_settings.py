"""Django settings for patchman project."""

import environ

env = environ.Env(
    DJANGO_DEBUG        = (bool, False),
    DJANGO_LOGLEVEL     = (str, "INFO"),
    ALLOWED_HOSTS       = (list, ['*']),
    SECRET_KEY          = (str),
    ADMIN_EMAIL         = (str),
    ADMIN_USERNAME      = (str),
    ADMIN_PASSWORD      = (str),
    DB_ENGINE           = (str, "sqlite3"),
    DB_HOST             = (str, ""),
    DB_PORT             = (int, ""),
    DB_NAME             = (str, "/app/db/sqlite.db"),
    DB_USER             = (str, ""),
    DB_PASSWORD         = (str, ""),
    TIME_ZONE           = (str),
    LANGUAGE_CODE       = (str),
    MAX_MIRRORS         = (int, 5),
    DAYS_WITHOUT_REPORT = (int, 14),
)

DEBUG = env("DJANGO_DEBUG")
LOGLEVEL = env("DJANGO_LOGLEVEL").upper()

ADMINS = (
    ('', f'{env("ADMIN_EMAIL")}'),
)

DATABASES = {
    "default": {
        "ENGINE": f"django.db.backends.{env('DB_ENGINE')}",
        "NAME": f"{env('DB_NAME')}",
        "USER": f"{env('DB_USER')}",
        "PASSWORD": f"{env('DB_PASSWORD')}",
        "HOST": f"{env('DB_HOST')}",
        "PORT": f"{env('DB_PORT')}",
        "STORAGE_ENGINE": "INNODB",
        "CHARSET" : "utf8"
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = env("TIME_ZONE")
USE_TZ    = len(env("TIME_ZONE")) > 0

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = env("LANGUAGE_CODE")

# Create a unique string here, and don't share it with anybody.
SECRET_KEY = env("SECRET_KEY")

# Add the IP addresses that your web server will be listening on
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Maximum number of mirrors to add or refresh per repo
MAX_MIRRORS = env("MAX_MIRRORS")

# Number of days to wait before notifying users that a host has not reported
DAYS_WITHOUT_REPORT = env("DAYS_WITHOUT_REPORT")

# Whether to run patchman under the gunicorn web server
RUN_GUNICORN = True

# Copy patchman media from these directories
STATICFILES_DIRS = ("/app/patchman/static/",)

# Enable Celery
USE_ASYNC_PROCESSING = True
CELERY_BROKER_URL    = "redis://redis:6379/0"

# Configure file-based cache
# Patchman appears to not utilise cache, despite instructing users to configure it.
# https://github.com/furlongm/patchman/issues/433
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",
    }
}
