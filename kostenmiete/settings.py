"""
Django settings for kostenmiete project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

# Edited Settings according to
# https://www.digitalocean.com/community/tutorials/how-to-deploy-django-to-app-platform

import os
import sys
import dj_database_url
from pathlib import Path
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# Get SECRET_KEY from env variable. If not available, generate one
# Attentions: If it's not in env variable, key changes with re-deployment
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
# Get it from env variable as String. If not defined -> "False".
# Compare retrieved String against "True". The result is the DEBUG Boolean
# only True, when env Variable == "True"
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

# Hosts defined in env variable and localhost are allowed
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Helper directive. Needed for example to determine the right database connection.
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kostenmiete.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kostenmiete.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
if DEVELOPMENT_MODE is True:
    # Get database sqlite3 from Django Project
    Databases = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
# When collecting static files, do not connect to database
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    # Exception, if no database env variable is set
    if os.getenv('DATABASE_URL', None) is None:
        raise Exception('DATABASE_URL environment variable not set')
    # Connect to database defined in env variable
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL')),
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'de-ch'

TIME_ZONE = 'Europe/Zurich'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
