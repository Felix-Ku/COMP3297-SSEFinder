"""
Django settings for CovidData project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path


from environs import Env ### /// Remove for local testing ///
env = Env() ### /// Remove for local testing ///
env.read_env() ### /// Remove for local testing ///

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/her

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'el3i&=il$i^d+_!shgqg2o%dq%n#42o1u*!)tx#vsd^ny5d#g%'

### /// Remove for local testing ///
SECRET_KEY = env('CHP_SECRET_KEY')  ### /// Remove for local testing ///

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['frozen-waters-91223.herokuapp.com', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'CovidDataPortal.apps.CoviddataportalConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'CovidData.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [BASE_DIR / 'templates']
        'DIRS': [str(BASE_DIR.joinpath('templates'))],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'geeks',
            ],
        },
    },
]

WSGI_APPLICATION = 'CovidData.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# /// Remove for local testing ///
DATABASES = {  ### /// Remove for local testing ///
'default': env.dj_db_url('DATABASE_URL')  ### /// Remove for local testing ///
}  ### /// Remove for local testing ///

# /// Unremove For local testing
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'location',
#         'USER': 'felix',
#         'PASSWORD': '12345',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# DATE_INPUT_FORMATS=['%d-%m-%Y']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))
LOGIN_REDIRECT_URL = '/'
