"""
Django settings for rapback project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Root of the project
PROJECT_ROOT = os.path.realpath(os.path.join(BASE_DIR, '..'))

# Heroku Settings
import dj_database_url
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ADMINS = (
    ('Michael Paris', 'mlparis92@gmail.com'),
)

MANAGERS = ADMINS

###### GET INSTANCE ID ######
INSTANCE_ID = 'rapchat.base'
#Try to get an i nstance id from the environment
if os.environ.get('INSTANCE_ID', None):
    INSTANCE_ID = os.environ.get('INSTANCE_ID', INSTANCE_ID)
else:
    print 'WARNING: The environment variable INSTANCE_ID is not set!'
    print 'Using default settings...'

# S3 SETTINGS
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

if INSTANCE_ID == 'LOCAL_VAGRANT':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'rapback_vagrant',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'TEST_NAME': 'rapchat_test',
            'USER': 'django_login',
            'PASSWORD': 'django_login',
            'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        }
    }
    AWS_STORAGE_BUCKET_NAME = 'rapback-vagrantbucket'
elif INSTANCE_ID == 'HEROKU':
    DATABASES = {
        'default': dj_database_url.config()
    }
elif INSTANCE_ID == 'PROD' :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': os.environ['RDS_DB_NAME'],                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': os.environ['RDS_PORT'],                      # Set to empty string for default.
        }
    }
elif INSTANCE_ID == 'PPE':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': os.environ['RDS_DB_NAME'],                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': os.environ['RDS_PORT'],                      # Set to empty string for default.
        }
    }
    AWS_STORAGE_BUCKET_NAME = 'rapbackppe-s3bucket'
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


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zilx(xz37t^k4!*43di!7#fp1hr6x5@2@28426(u8@4$s1_)2#'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Open source code
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'django_extensions',
    'gunicorn',
    # My apps
    'rapback',
    'users',
    'core',
    # 'crowds',
    'groupsessions',
    'feedback',
    # 'video_stitching',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'rapback.middleware.ProfileMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'rapback.urls'

WSGI_APPLICATION = 'rapback.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

AUTH_USER_MODEL = 'users.Profile'

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


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
