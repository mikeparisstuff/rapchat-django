# Django settings for rapchat project.

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Michael Paris', 'mlparis92@gmail.com'),
)

INSTANCE_ID = 'rapchat.base'

#Try to get an i nstance id from the environment
if os.environ.get('INSTANCE_ID', None):
    INSTANCE_ID = os.environ.get('INSTANCE_ID', INSTANCE_ID)
else:
    print 'WARNING: The environment variable INSTANCE_ID is not set!'
    print 'Using default settings...'


#Root to base of this directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Root of the project
PROJECT_ROOT = os.path.realpath(os.path.join(BASE_DIR, '..'))

MANAGERS = ADMINS

# Heroku Settings
import dj_database_url
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# S3 SETTINGS
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJ2KVSZDJH7UPGAAQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'rapback'

if INSTANCE_ID == 'LOCAL_VAGRANT':
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    #         'NAME': 'rapchat_dev',                      # Or path to database file if using sqlite3.
    #         # The following settings are not used with sqlite3:
    #         'TEST_NAME': 'rapchat_test',
    #         'USER': 'django_login',
    #         'PASSWORD': 'django_login',
    #         'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
    #         'PORT': '',                      # Set to empty string for default.
    #     }
    # }
    DATABASES = {
        'default' : {
            'ENGINE' : 'django.db.backends.postgresql_psycopg2',
            'NAME' : 'd20vr0sil2d4oe',
            'USER' : 'ryatbdsdjdnvzu',
            'HOST' : 'ec2-54-235-152-22.compute-1.amazonaws.com',
            'PORT' : '5432',
            'PASSWORD' : 'i5RJ664vXlOZ2KOj8lBSUFWz-s'
        }
    }
elif INSTANCE_ID == 'HEROKU':
    DATABASES = {
        'default': dj_database_url.config()
    }
elif INSTANCE_ID == 'Prod' :
    DATABASES = {
	'default': {
	  'ENGINE': 'django.db.backends.postgresql_psycopg2',
	  'NAME': 'rapchat_prod',
	  'USER': 'rapback1',
	  'PASSWORD': os.environ.get('DB_PW'),
	  'HOST': 'localhost',
	  'PORT': '',
	}
    }
elif INSTANCE_ID == 'PPE':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'RapbackPPE',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'rapback_admin',
            'PASSWORD': "kB1fo6TCb|8vQt!FAz)nj]~mly6'I",
            'HOST': 'rapbackppe.cdgnmiiuczg0.us-west-2.rds.amazonaws.com',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '5432',                      # Set to empty string for default.
        }
    }
    AWS_STORAGE_BUCKET_NAME = 'rapbackppe'
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'NAME',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'USER',
            'PASSWORD': "PASSWORD",
            'HOST': 'HOST',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '5432',                      # Set to empty string for default.
        }
    }



# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = 'staticfiles'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ds^!hv%$0n9&uvmoalm&kdx$9f!*ycib&4h3!xy*yuv50bo$t)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'rapchat.middleware.ProfileMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'rapchat.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'rapchat.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'PAGINATE_BY': 1,
}

AUTH_PROFILE_MODULE = 'users.Profile'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'grappelli',
    'django.contrib.admin',
    # 'django.contrib.admindocs',

    # Open source code
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'south',
    'django_nose',
    'django_extensions',

    # My apps
    'users',
    'core',
    'crowds',
    'groupsessions',
    'feedback',
    # 'video_stitching',
)

SWAGGER_SETTINGS = {
    "exclude_namespaces": [],
    "api_version": '0.2',
    "api_key": '',
    "enabled_methods": [
        'get',
        'post',
        'put',
    ]
}


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

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
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
