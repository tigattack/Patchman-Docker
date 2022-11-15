#!/bin/sh -e

# Set default values
DEFAULT_CELERY_REDIS_HOST="redis"
DEFAULT_CELERY_REDIS_PORT="6379"
DEFAULT_CELERY_LOG_LEVEL="INFO"
DEFAULT_GUNICORN_WORKERS="2"

if [ "$1" = "worker" ]; then

  # Set celery host & port to defaults if unset
  if [ -z "$CELERY_REDIS_HOST" ]; then
    export CELERY_REDIS_HOST="$DEFAULT_CELERY_REDIS_HOST"
  fi
  if [ -z "$CELERY_REDIS_PORT" ]; then
    export CELERY_REDIS_PORT="$DEFAULT_CELERY_REDIS_PORT"
  fi

  # Set celery log level to default if unset
  if [ -z "$CELERY_LOG_LEVEL" ]; then
    export CELERY_LOG_LEVEL="$DEFAULT_CELERY_LOG_LEVEL"
  else
    export CELERY_LOG_LEVEL="$(echo $CELERY_LOG_LEVEL | tr '[a-z]' '[A-Z]')"
  fi

  # Run celery
  C_FORCE_ROOT=1 celery -b redis://${CELERY_REDIS_HOST}:${CELERY_REDIS_PORT}/0 -A patchman worker -l "$CELERY_LOG_LEVEL" -E

elif [ "$1" = "server" ]; then

  # Prepare DB & app
  ./manage.py makemigrations
  ./manage.py migrate --run-syncdb
  ./manage.py collectstatic --noinput --clear

  # Create Django superuser
  # This exists because there's no '--noinput' flag in Django 2, which patchman is based on.
  echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='$ADMIN_EMAIL', is_superuser=True).delete(); User.objects.create_superuser('$ADMIN_USERNAME', '$ADMIN_EMAIL', '$ADMIN_PASSWORD')" | ./manage.py shell

  # Set number of workers to default if unset
  if [ -z "$GUNICORN_WORKERS" ]; then
    GUNICORN_WORKERS="$DEFAULT_GUNICORN_WORKERS"
  fi

  # Run gunicorn for patchman
  gunicorn --bind 0.0.0.0:80 --workers "$GUNICORN_WORKERS" patchman.wsgi:application

else
  echo "Unknown command: $1"
fi
