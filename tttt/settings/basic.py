# Django settings for tttt project.

import os
import sys

from django.conf import global_settings

ROOT_PATH = os.path.abspath("%s/%s/" %
                            (os.path.dirname(os.path.realpath(__file__)), "../.."))

DEBUG = True

VERSION = "1.1.0"

ADMINS = (
    # ('Example', 'admin@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or
        # 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Or path to database file if using sqlite3.
        'NAME': os.path.join(ROOT_PATH, 'data.db'),
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Prague'

DATETIME_FORMAT = 'Y-m-d H:i'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = "%s/tttt/%s/" % (ROOT_PATH, 'static')

STORAGE_ROOT = "%s/%s/" % (ROOT_PATH, 'storage')

STORAGE_URL = "/storage/"

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL to gitweb
GITWEB_URL = '/gitweb/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "%s/%s/" % (ROOT_PATH, 'tttt/media'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.PersistentRemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
)

# Cache only for production deployment
# CACHES = {
#    'default': {
#'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#'LOCATION': 'unique-snowflake'
# If following code will be set, you need run ./manage.py createcachetable gt_cache_table
#'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#'LOCATION': 'gt_cache_table',
#    }
#}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            "%s/%s/" % (ROOT_PATH, 'tttt/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'tttt.context_processors.basic',
            ],
            'debug': DEBUG,
        },
    },
]

TASKOMATIC_HOOKS = (
    'apps.core.management.commands',
)

ROOT_URLCONF = 'tttt.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'tttt.wsgi.application'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'widget_tweaks',
    'rest_framework',
    'django_filters',
    'taggit',
    'reversion',
    'crispy_forms',
    'apps.core',
    'apps.taskomatic',
    'apps.waiver',
    'apps.kerberos',
    'apps.api',
    'apps.report',
)

try:
    import django_extensions
    INSTALLED_APPS += (
        "django_extensions",
    )
except ImportError:
    pass


ENABLE_PLUGINS = (
    #       "irc",
    "backuplogs",
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s.%(funcName)s'
                      '(line no. %(lineno)d): %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(module)s.%(funcName)s(%(lineno)d): '
                      '%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        # 'logfile': {
        #     'level': 'ERROR',
        #     'class': 'logging.handlers.WatchedFileHandler',
        #     'filename': ROOT_PATH + '/log/error.log',
        #     'formatter': 'verbose'
        # },
        # 'infofile': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.WatchedFileHandler',
        #     'filename': ROOT_PATH + '/log/info.log',
        #     # 'formatter': 'verbose'
        # },
        'elasticsearch': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'mail_admins'],
        'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
    },
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'PAGE_SIZE': 100
}


### Kerberos ###
# kerberos realm and service
KRB5_REALM = 'EXAMPLE.COM'
KRB5_SERVICE = 'krbtgt@AS.EXAMPLE.COM'
DEFAULT_KERBEROS_PASSWORD = "password"

### Web UI ###
# redirect url after login
LOGIN_REDIRECT_URL = '/'

PAGINATOR_OBJECTS_ONPAGE = 20
PAGINATOR_OBJECTS_ONHOMEPAGE = 10
CHECK_COMMMITS_PREVIOUS_DAYS = 7

GRAPPELLI_ADMIN_TITLE = "Green Tea"
GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

# How many periods are shown on web ui
RANGE_PREVIOUS_RUNS = 9

CHART_MAX_DAYS = 30

# How many picked tasks are stored
MAX_TASKOMATIC_HISTORY = 1000

TAGGIT_CASE_INSENSITIVE = True
GIT_TREE_PARRENT = "%s/tree/master/%s"

TEMPLATE_FOOTER = "Created by Satellite QA Team in 2013-2017"


### BEAKER ###
BEAKER_SERVER = "https://beaker.example.com"

# Set BEAKER_OWNER and BEAKER_PASS or you can use kerberos auth
BEAKER_OWNER = None
BEAKER_PASS = None
BEAKER_JOB_GROUP = ""  # the group must to exist in Beaker

BEAKER_DEFAULT_PACKAGES = (
    # "vim", "gcc", "make"
)

# How long should <reservesys> block the machine
BEAKER_RESERVESYS = 86400
MAX_LOGS_IN_ONE_CHECK = 1000
RESERVE_TEST = "/distribution/reservesys"
BROKEN_SYSTEM_DAYS = 7

### Elasticserach ###
ELASTICSEARCH = ()
ELASTICSEARCH_MAX_SIZE = 10**6  # 10MB
LOGFILE_LIFETIME = 30

# Time period for which average run time of tests should be computed, in hours
LONGEST_RUNNING_PERIOD = 168
LONGEST_RUNNING_COLUMN_LENGTH = 15


### DEBUGING ###
if int(os.environ.get("DDD", 0)) > 0:
    # LOGGING['loggers']['commands']['handlers'] = ['console', ]
    # LOGGING['loggers']['commands']['propagate'] = False
    # LOGGING['root']['handlers'].append('console')

    # Enabling django-debug-toolbar..."
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
    INSTALLED_APPS += ('debug_toolbar',)
