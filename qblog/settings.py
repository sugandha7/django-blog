"""
Django settings for qblog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# Parse database configuration from $DATABASE_URL
import dj_database_url


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'k@%r38ivoq!85^+9(x)&y0+3p(*mizjd_-cztf*6irs*x-#g12'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

#Add the path to your templates directory here.
TEMPLATE_PATH = os.path.join(BASE_DIR, 'blog/templates')
TEMPLATE_DIRS = [TEMPLATE_PATH,]

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'gunicorn',
    'django_markdown',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
#Add the path to your urls.py here.
ROOT_URLCONF = 'qblog.urls'

#Add the path to your wsgi.py here.
WSGI_APPLICATION = 'qblog.wsgi.application'


# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {'default' : dj_database_url.config() }

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Kolkata'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

USE_L10N = True

USE_TZ = True


# URL that handles the media served from STATIC_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/static/"
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#Add the path to your static files (css, javascript, html) here.
STATIC_PATH = os.path.join(BASE_DIR,'blog/static')
STATICFILES_DIRS = (
    STATIC_PATH,
)
