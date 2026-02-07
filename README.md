# Docker Patchman

This is a Dockerised version of [Patchman](https://github.com/furlongm/patchman).

It also has a modified host page to add a separate section for security updates.

## Getting Started

1. Download `docker-compose.yml` and `.env`
2. Add your configuration in `.env` (see [Environment Variables](#environment-variables) below)
3. Run `docker compose up -d` or `docker-compose up -d` (old version)
4. Run `docker compose exec -it server patchman-manage createsuperuser` and enter the same ADMIN details you configured in `.env`
5. Run `docker compose logs mariadb 2>&1 | grep GENERATED` to get your generated MariaDB root password. Store this somewhere safe.
6. Browse to `<IP/hostname>:8080` and start using Patchman!

For next steps, you'll need to configure your Patchman clients. You can find instructions in the [Patchman](https://github.com/furlongm/patchman) repository.

### Scheduled Maintenance

The supplied `docker-compose.yml` includes a `scheduler` service which executes Patchman maintenance operations on a predefined schedule.

If the scheduler encounters any errors when performing Patchman maintenance, it will save logs to `./scheduler-error-logs`. You can also configure Slack and SMTP notifications; see [here](https://github.com/mcuadros/ofelia#logging) for information.

See the [Environment Variables](#environment-variables) section below for the default schedule and how to change it to your preference.

Patchman maintenance (executed with `patchman -a`) includes the following operations:

- Refresh repositories
- Find host updates
- Process pending reports\*
- Clean reports (removes all but the last three reports from each host)
- Perform some sanity checks on the database and clean unused entries
- Perform reverse DNS checks if enabled per-host

_\* Reports should rarely, if ever, be pending for any significant duration since they are expected to be processed by the `worker` service in an asynchronous manner upon subsmission._

### MySQL/MariaDB

By default, the MariaDB database included in `docker-compose.yml` will use a randomly generated root password.

If you wish to set your own password, configure a `MYSQL_ROOT_PASSWORD` environment variable in `docker-compose.yml`.

## Environment variables

This Docker image supports configuring any Patchman setting through environment variables. The configuration system intelligently handles type casting for booleans, integers, lists, and dictionaries.

### Configuration Methods

1. **Direct Setting Override**: Use the exact setting name from Patchman's configuration
   - Example: `MAX_MIRRORS=10`, `DAYS_WITHOUT_REPORT=7`

2. **List Values**: Provide comma-separated strings for list-type settings
   - Example: `ERRATA_OS_UPDATES=rocky,alma,ubuntu`, `ALMA_RELEASES=8,9,10`

3. **Wildcard Override**: Use `PATCHMAN_SETTING_<NAME>=<value>` for any custom setting
   - Example: `PATCHMAN_SETTING_CUSTOM_VALUE=123`

For a complete list of available Patchman settings and their descriptions, refer to the [upstream local_settings.py](https://github.com/furlongm/patchman/blob/main/etc/patchman/local_settings.py).

### Common Environment Variables

| Name                            | Description                                                                                                          | Default                                                |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| `ADMIN_EMAIL`                   | Administrator email address.                                                                                         | `admin@example.com`                                    |
| `ADMIN_USERNAME`                | Administrator username.                                                                                              | `admin`                                                |
| `SECRET_KEY`                    | Django secret key. Create a unique string and don't share it with anybody.                                          | _Required for production_                              |
| `TIME_ZONE`                     | Time zone for this installation. See [TZ database](http://en.wikipedia.org/wiki/List_of_tz_zones_by_name).          | `Etc/UTC`                                              |
| `LANGUAGE_CODE`                 | Language code. See [language identifiers](http://www.i18nguy.com/unicode/language-identifiers.html).                | `en-GB`                                                |
| `MAX_MIRRORS`                   | Maximum number of mirrors to add or refresh per repo.                                                               | `5`                                                    |
| `MAX_MIRROR_FAILURES`           | Maximum number of failures before disabling a mirror. Set to `-1` to never disable.                                 | `14`                                                   |
| `DAYS_WITHOUT_REPORT`           | Number of days to wait before notifying users that a host has not reported.                                         | `14`                                                   |
| `ALLOWED_HOSTS`                 | Comma-separated list of hosts allowed to access Patchman.                                                           | `*` (all hosts)                                        |
| `CSRF_TRUSTED_ORIGINS`          | Comma-separated list of trusted origins for CSRF protection.                                                        | `http://localhost`                                     |
| `ERRATA_OS_UPDATES`             | Comma-separated list of errata sources to update.                                                                   | `yum,rocky,alma,arch,ubuntu,debian`                    |
| `ALMA_RELEASES`                 | Comma-separated list of Alma Linux releases to update.                                                              | `8,9,10`                                               |
| `DEBIAN_CODENAMES`              | Comma-separated list of Debian codenames to update.                                                                 | `bookworm,trixie`                                      |
| `UBUNTU_CODENAMES`              | Comma-separated list of Ubuntu codenames to update.                                                                 | `jammy,noble`                                          |
| `PATCHMAN_MAINTENANCE_ENABLED`  | Enable/disable the scheduled maintenance action.                                                                    | `true`                                                 |
| `PATCHMAN_MAINTENANCE_SCHEDULE` | Cron schedule for maintenance. See [go-cron format](https://pkg.go.dev/github.com/robfig/cron).                     | `@daily`                                               |

### Database Configuration

By default, Patchman will use the database container included in `docker-compose.yml`.

However, you can use an external/different database if you wish. To do so, configure `.env` with the following settings:

| Name          | Description                                                             | Default                 |
| ------------- | ----------------------------------------------------------------------- | ----------------------- |
| `DB_ENGINE`   | Supported database engines: `mysql`, `oracle`, and `postgresql`.        | `mysql`                 |
| `DB_HOST`     | Database server IP/name.                                                | `mariadb`               |
| `DB_PORT`     | Database port. If empty, will use the default port for selected engine. |                         |
| `DB_NAME`     | Database name.                                                          | `patchman`              |
| `DB_USER`     | Database username.                                                      | `patchman`              |
| `DB_PASSWORD` | Database password.                                                      | `MyPatchmanDBP@ssw0rd!` |

### Advanced Configuration & Debugging

| Name                | Description                                                                                        | Default |
| ------------------- | -------------------------------------------------------------------------------------------------- | ------- |
| `DJANGO_DEBUG`      | Enable/disable Django debug.                                                                       | `False` |
| `DJANGO_LOGLEVEL`   | Set Django's log level.                                                                            | `INFO`  |
| `GUNICORN_WORKERS`  | Numbers of Gunicorn (web server) workers.                                                          | `2`     |
| `CELERY_REDIS_HOST` | Redis server IP/name for Celery worker.<br>Only set this if you want to use your own redis server. | `redis` |
| `CELERY_REDIS_PORT` | Redis server port for Celery worker.<br>Only set this if you want to use your own redis server.    | `6379`  |
| `CELERY_LOG_LEVEL`  | Set Celery's log level.                                                                            | `INFO`  |

## Credits

- [Patchman](https://github.com/furlongm/patchman)
- [Original docker-patchman](https://github.com/uqlibrary/docker-patchman) (unmaintained)
