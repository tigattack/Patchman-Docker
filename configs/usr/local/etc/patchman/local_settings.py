"""Django settings for patchman project."""

import environ

env = environ.Env(
    DJANGO_DEBUG         = (bool, False),
    DJANGO_LOGLEVEL      = (str, "INFO"),
    ALLOWED_HOSTS        = (list, ['*']),
    CSRF_TRUSTED_ORIGINS = (list, ["http://localhost"]),
    SECRET_KEY           = (str),
    ADMIN_EMAIL          = (str),
    ADMIN_USERNAME       = (str),
    DB_ENGINE            = (str),
    DB_HOST              = (str),
    DB_PORT              = (int, ""),
    DB_NAME              = (str),
    DB_USER              = (str),
    DB_PASSWORD          = (str),
    TIME_ZONE            = (str, "Etc/UTC"),
    LANGUAGE_CODE        = (str, "en-GB"),
    MAX_MIRRORS          = (int, 5),
    DAYS_WITHOUT_REPORT  = (int, 14),
    CELERY_REDIS_HOST    = (str),
    CELERY_REDIS_PORT    = (str),
    ERRATA_OS_UPDATES    = (list, ["yum", "rocky", "alma", "arch", "ubuntu", "debian"]),
)

DEBUG = env("DJANGO_DEBUG")
LOGLEVEL = env("DJANGO_LOGLEVEL").upper()

ADMINS = (
    (f'{env("ADMIN_USERNAME")}', f'{env("ADMIN_EMAIL")}'),
)

DATABASES = {
    "default": {
        "ENGINE": f"django.db.backends.{env('DB_ENGINE')}",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "STORAGE_ENGINE": "INNODB",
        "CHARSET": "utf8",
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = env("TIME_ZONE")
USE_TZ    = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = env("LANGUAGE_CODE")

# Create a unique string here, and don't share it with anybody.
SECRET_KEY = env("SECRET_KEY")

# Add the IP addresses that your web server will be listening on
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Trusted origins for CSRF protection
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS")

# Maximum number of mirrors to add or refresh per repo
MAX_MIRRORS = env("MAX_MIRRORS")

# Number of days to wait before notifying users that a host has not reported
DAYS_WITHOUT_REPORT = env("DAYS_WITHOUT_REPORT")

# Whether to run patchman under the gunicorn web server
RUN_GUNICORN = True

# Copy patchman media from these directories
STATIC_ROOT = ("/app/patchman/static/",)

# Enable Celery
USE_ASYNC_PROCESSING = True
CELERY_BROKER_URL    = f"redis://{env('CELERY_REDIS_HOST')}:{env('CELERY_REDIS_PORT')}/0"

# List of update types to consider when generating errata reports
ERRATA_OS_UPDATES = env("ERRATA_OS_UPDATES")
