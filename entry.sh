#!/bin/sh -e

# Create sqlite DB dir if using sqlite.
if [ -z "$DB_ENGINE" -o "$DB_ENGINE" = "sqlite3" ]; then
  if [ -z "$DB_NAME" ]; then
    DBDIR="${APPDIR}/db"
  elif [ "$DB_NAME" ]; then
    DBDIR=$(dirname "$DB_NAME")
  fi
  if [ ! -d "$DBDIR" ]; then
    mkdir "$DBDIR"
  fi
fi

# Prepare DB & app
./manage.py makemigrations
./manage.py migrate --run-syncdb
./manage.py collectstatic --noinput --clear

# Create Django superuser
# This exists because there's no '--noinput' flag in Django 2, which patchman is based on.
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='$ADMIN_EMAIL', is_superuser=True).delete(); User.objects.create_superuser('$ADMIN_USERNAME', '$ADMIN_EMAIL', '$ADMIN_PASSWORD')" | ./manage.py shell

# Default number of workers if unspecified
if [ -z "$GUNICORN_WORKERS" ]; then
  GUNICORN_WORKERS=2
fi

# Start Patchman
gunicorn --bind 0.0.0.0:80 --workers "$GUNICORN_WORKERS" patchman.wsgi:application
