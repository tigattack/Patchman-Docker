# Django settings for patchman project.

#DEBUG = False
DEBUG = True

ADMINS = (
    ('{ADMINNAME}', '{ADMINEMAIL}'),
)

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
       'NAME': '{DBNAME}',                   # Or path to database file if using sqlite3.
       'USER': '{DBUSER}',                   # Not used with sqlite3.
       'PASSWORD': '{DBPW}',               # Not used with sqlite3.
       'HOST': '{DBHOST}',                           # Set to empty string for localhost. Not used with sqlite3.
       'PORT': '',                           # Set to empty string for default. Not used with sqlite3.
       'STORAGE_ENGINE': 'INNODB',
       'CHARSET' : 'utf8'
   }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Australia/Brisbane'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# Create a unique string here, and don't share it with anybody.
SECRET_KEY = '{SECRETKEY}'

# Add the IP addresses that your web server will be listening on,
# instead of '*'
ALLOWED_HOSTS = ['127.0.0.1', '*']
#ALLOWED_HOSTS = ['127.0.0.1', '192.168.56.102']

# Maximum number of mirrors to add or refresh per repo
MAX_MIRRORS = 2

# Number of days to wait before notifying users that a host has not reported
DAYS_WITHOUT_REPORT = 14

# Whether to run patchman under the gunicorn web server
RUN_GUNICORN = True

# Copy patchman media from these directories
#STATICFILES_DIRS = ('/patchman/static/',)

# Enable memcached
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#    }
#}
