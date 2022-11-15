# Docker Patchman

This is a Dockerised version of [Patchman](https://github.com/furlongm/patchman).

It also has a modified host page to add a separate section for security updates.

## Environment variables

All environment variables without a default are **required**, unless noted otherwise in the variable's description.

The rest are optional and, if unspecified, will use the listed default.

| Name                  | Description                                                                                                                                                                                                                                   | Default           |
|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| `ADMIN_EMAIL`         | Administrator email address.                                                                                                                                                                                                                  |                   |
| `ADMIN_USERNAME`      | Administrator username.                                                                                                                                                                                                                       |                   |
| `ADMIN_PASSWORD`      | Administrator password.                                                                                                                                                                                                                       |                   |
| `SECRET_KEY`          | Patchman's secret key. Create a unique string and don't share it with anybody.                                                                                                                                                                |                   |
| `DB_ENGINE`           | Supported database engines: `mysql`, `oracle`, and `postgresql`.                                                                                                                                                                              |                   |
| `DB_HOST`             | Database server IP/name.                                                                                                                                                                                                                      |                   |
| `DB_PORT`             | Database port.                                                                                                                                                                                                                                |                   |
| `DB_NAME`             | Database name or path to file if using `sqlite3`.                                                                                                                                                                                             |                   |
| `DB_USER`             | Database username.                                                                                                                                                                                                                            |                   |
| `DB_PASSWORD`         | Database password.                                                                                                                                                                                                                            |                   |
| `TIME_ZONE`           | Time zone for this installation. All choices can be found [here](http://en.wikipedia.org/wiki/List_of_tz_zones_by_name).<br>At time of writing, Patchman does not properly support this. It will work, but you'll receive warnings to STDOUT. | `America/NewYork` |
| `LANGUAGE_CODE`       | Language for this installation. All choices can be found [here](http://www.i18nguy.com/unicode/language-identifiers.html).                                                                                                                    | `en-US`           |
| `MAX_MIRRORS`         | Maximum number of mirrors to add or refresh per repo.                                                                                                                                                                                         | `5`               |
| `DAYS_WITHOUT_REPORT` | Number of days to wait before notifying users that a host has not reported.                                                                                                                                                                   | `14`              |
| `ALLOWED_HOSTS`       | Hosts allowed to access Patchman.                                                                                                                                                                                                             | `*`               |
| `DJANGO_DEBUG`        | Enable/disable Django debug.                                                                                                                                                                                                                  | `False`           |
| `DJANGO_LOGLEVEL`     | Set Django's log level.                                                                                                                                                                                                                       | `INFO`            |
| `GUNICORN_WORKERS`    | Numbers of Gunicorn (web server) workers.                                                                                                                                                                                                     | `2`               |
| `CELERY_REDIS_HOST`   | Redis server IP/name for Celery worker.<br>Only set this if you want to use your own redis server.                                                                                                                                            | `redis`           |
| `CELERY_REDIS_PORT`   | Redis server port for Celery worker.<br>Only set this if you want to use your own redis server.                                                                                                                                               | `6379`            |
| `CELERY_LOG_LEVEL`    | Set Celery's log level.                                                                                                                                                                                                                       | `INFO`            |

## MySQL DB config

Note you can use any of the supported databases listed above, this is just an example for preparing MySQL for Patchman.

The following MySQL commands should be run (after replacing passwords etc.) on your database prior to starting up your container.

```
mysql> CREATE DATABASE patchman CHARACTER SET utf8 COLLATE utf8_general_ci;
Query OK, 1 row affected (0.00 sec)

mysql> GRANT ALL PRIVILEGES ON patchman.* TO patchman@'%' IDENTIFIED BY 'coolpw';
Query OK, 0 rows affected (0.00 sec)
```

## Credits

- [Patchman](https://github.com/furlongm/patchman)
- [Original docker-patchman](https://github.com/uqlibrary/docker-patchman) (unmaintained)
