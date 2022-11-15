#!/bin/sh -e

echo "$1" > /tmp/container-mode

if [ "$1" = "worker" ]; then

  # Ensure celery log level is uppercase
  export CELERY_LOG_LEVEL="$(echo $CELERY_LOG_LEVEL | tr '[a-z]' '[A-Z]')"

  # Add celery user if it doesn't exist
  id -u celery >/dev/null 2>&1 || adduser -S celery
  # Get celery user id
  celery_uid="$(id -u celery)"

  # Run celery
  celery -b redis://${CELERY_REDIS_HOST}:${CELERY_REDIS_PORT}/0 -A patchman worker -l "$CELERY_LOG_LEVEL" -E --uid $celery_uid

elif [ "$1" = "server" ]; then

  # Prepare DB
  ${APPDIR}/manage.py migrate --run-syncdb
  # Quietly collect static files
  ${APPDIR}/manage.py collectstatic --noinput --clear >/dev/null

  # Run gunicorn for patchman
  gunicorn --bind 0.0.0.0:80 --workers "$GUNICORN_WORKERS" patchman.wsgi:application

else
  echo "Unknown command: $1"
  exit 1
fi
