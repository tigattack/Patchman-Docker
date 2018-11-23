#!/bin/bash
CONFIGFILE=/etc/patchman/local_settings.py
# Ensure our variables are set
for i in ADMINNAME ADMINEMAIL ADMINACC ADMINPW DBNAME DBUSER DBPW DBHOST SECRETKEY; do
  if [ -z ${!i} ]; then
    echo "$i is not set. Exiting."
    exit 1
  else
    # Replace config file variables
    sed -i "s/{$i}/${!i}/g" $CONFIGFILE;
  fi
done

patchman-manage makemigrations
patchman-manage migrate

cp -r /patchman/media/* /patchman/static/
cp -r /usr/lib/python2.7/site-packages/Django*/django/contrib/admin/static/* /patchman/static/

# This exists because django's createsuperuser command does not allow setting password without console input
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='$ADMINEMAIL', is_superuser=True).delete(); User.objects.create_superuser('$ADMINACC', '$ADMINEMAIL', '$ADMINPW')" | patchman-manage shell

gunicorn patchman.wsgi -b 0.0.0.0:80
