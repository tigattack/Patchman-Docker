"""Django settings for patchman project."""

import os
import environ
from datetime import timedelta
from celery.schedules import crontab

env = environ.Env()


# Helper function to get environment variable with optional default
def env_get(key, default=None, cast=None):
    """Get environment variable with optional type casting."""
    value = os.environ.get(key)
    if value is None:
        return default
    if cast is None:
        return value
    if cast is bool:
        return value.lower() in ("true", "1", "yes", "on")
    if cast is int:
        return int(value)
    if cast is list:
        # Support comma-separated lists
        return [item.strip() for item in value.split(",") if item.strip()]
    if cast is dict:
        # Support JSON-formatted dicts
        import json

        return json.loads(value)
    return cast(value)


# Core Django Settings
DEBUG = env_get("DJANGO_DEBUG", False, bool)

ADMINS = (
    (env_get("ADMIN_USERNAME", "admin"), env_get("ADMIN_EMAIL", "admin@example.com")),
)

# Database Configuration
DATABASES = {
    "default": {
        "ENGINE": f"django.db.backends.{env_get('DB_ENGINE', 'sqlite3')}",
        "NAME": env_get("DB_NAME", "/var/lib/patchman/db/patchman.db"),
        "USER": env_get("DB_USER", ""),
        "PASSWORD": env_get("DB_PASSWORD", ""),
        "HOST": env_get("DB_HOST", ""),
        "PORT": env_get("DB_PORT", "", int) or "",
        "STORAGE_ENGINE": env_get("DB_STORAGE_ENGINE", "INNODB"),
        "CHARSET": env_get("DB_CHARSET", "utf8"),
    }
}

# Localization
TIME_ZONE = env_get("TIME_ZONE", "Etc/UTC")
USE_TZ = env_get("USE_TZ", True, bool)
LANGUAGE_CODE = env_get("LANGUAGE_CODE", "en-GB")

# Security
SECRET_KEY = env_get("SECRET_KEY", "")
ALLOWED_HOSTS = env_get("ALLOWED_HOSTS", ["*"], list)
CSRF_TRUSTED_ORIGINS = env_get("CSRF_TRUSTED_ORIGINS", ["http://localhost"], list)

# Patchman-specific Settings
MAX_MIRRORS = env_get("MAX_MIRRORS", 5, int)
MAX_MIRROR_FAILURES = env_get("MAX_MIRROR_FAILURES", 14, int)
DAYS_WITHOUT_REPORT = env_get("DAYS_WITHOUT_REPORT", 14, int)

# Errata Configuration
ERRATA_OS_UPDATES = env_get(
    "ERRATA_OS_UPDATES", ["yum", "rocky", "alma", "arch", "ubuntu", "debian"], list
)
ALMA_RELEASES = env_get("ALMA_RELEASES", [8, 9, 10], list)
DEBIAN_CODENAMES = env_get("DEBIAN_CODENAMES", ["bookworm", "trixie"], list)
UBUNTU_CODENAMES = env_get("UBUNTU_CODENAMES", ["jammy", "noble"], list)

# Web Server
RUN_GUNICORN = env_get("RUN_GUNICORN", True, bool)
STATIC_ROOT = env_get("STATIC_ROOT", "/app/patchman/static/")

# Caching
cache_backend = env_get("CACHE_BACKEND", "django.core.cache.backends.redis.RedisCache")
cache_location = env_get(
    "CACHE_LOCATION",
    f"redis://{env_get('CELERY_REDIS_HOST', 'redis')}:{env_get('CELERY_REDIS_PORT', '6379')}",
)
CACHES = {
    "default": {
        "BACKEND": cache_backend,
        "LOCATION": cache_location,
    }
}
CACHE_MIDDLEWARE_SECONDS = env_get("CACHE_MIDDLEWARE_SECONDS", 0, int)

# Celery Configuration
USE_ASYNC_PROCESSING = env_get("USE_ASYNC_PROCESSING", True, bool)
CELERY_BROKER_URL = env_get(
    "CELERY_BROKER_URL",
    f"redis://{env_get('CELERY_REDIS_HOST', 'redis')}:{env_get('CELERY_REDIS_PORT', '6379')}/0",
)

# Celery Beat Schedule (can be overridden via environment)
CELERY_BEAT_SCHEDULE = env_get(
    "CELERY_BEAT_SCHEDULE",
    {
        "process_all_unprocessed_reports": {
            "task": "reports.tasks.process_reports",
            "schedule": crontab(minute="*/5"),
        },
        "refresh_repos_daily": {
            "task": "repos.tasks.refresh_repos",
            "schedule": crontab(hour=4, minute=0),
        },
        "update_errata_cves_cwes_every_12_hours": {
            "task": "errata.tasks.update_errata_and_cves",
            "schedule": timedelta(hours=12),
        },
        "run_database_maintenance_daily": {
            "task": "util.tasks.clean_database",
            "schedule": crontab(hour=6, minute=0),
        },
        "remove_old_reports": {
            "task": "reports.tasks.remove_reports_with_no_hosts",
            "schedule": timedelta(days=7),
        },
        "find_host_updates": {
            "task": "hosts.tasks.find_all_host_updates_homogenous",
            "schedule": timedelta(hours=24),
        },
    },
    dict,
)

# Logging Configuration
log_level = env_get("DJANGO_LOGLEVEL", "INFO").upper()
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": log_level,
    },
    "loggers": {
        "urllib3": {"level": "WARNING", "handlers": ["console"], "propagate": False},
        "git": {"level": "WARNING", "handlers": ["console"], "propagate": False},
        "version_utils": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False,
        },
        "celery": {"level": "WARNING", "handlers": ["console"], "propagate": False},
    },
}

# Allow any additional settings to be overridden via environment variables
# Format: PATCHMAN_SETTING_<SETTING_NAME>=<value>
for key, value in os.environ.items():
    if key.startswith("PATCHMAN_SETTING_"):
        setting_name = key.replace("PATCHMAN_SETTING_", "")
        # Try to evaluate as Python literal, fall back to string
        try:
            import ast

            globals()[setting_name] = ast.literal_eval(value)
        except (ValueError, SyntaxError):
            globals()[setting_name] = value
