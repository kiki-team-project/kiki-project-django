"""
Django settings for kikiproject project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import os, json
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

secret_file = os.path.join(BASE_DIR, 'secrets.json')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")
KK_API_KEY = os.environ.get("KK_API_KEY")
EMAIL_HOST_USER = os.environ.get("EMAIL")
EMAIL_HOST_PASSWORD = os.environ.get("PASSWORD")
DEFAULT_FROM_MAIL = EMAIL_HOST_USER
FRONT_BASE_URL = "http://127.0.0.1:5500"
BACKEND_BASE_URL = "http://127.0.0.1:8000"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = os.environ.get("DEBUG", "0")

# # DEBUG == "1" 이면 배포환경 "0" 이면 개발환경.
# if DEBUG == "1":
#     DEBUG = False
#     ALLOWED_HOSTS = [
#         "localhost",
#         "backend",
#         "https://cookai.today",
#         "https://www.backend.cookai.today",
#     ]
#     KK_API_KEY = os.environ.get("KK_DEPLOY_API_KEY")
#     FRONT_BASE_URL = "https://cookai.today"
#     BACKEND_BASE_URL = "https://www.backend.cookai.today"
#     CORS_ALLOWED_ORIGINS = [
#         "https://cookai.today",
#         "https://www.backend.cookai.today",
#     ]
#     CSRF_TRUSTED_ORIGINS = [
#         "https://cookai.today",
#         "https://www.backend.cookai.today",
#     ]

# elif DEBUG == "0":
#     DEBUG = True
#     ALLOWED_HOSTS = [
#         "backend",
#         "localhost",
#         "127.0.0.1",
#     ]
#     KK_API_KEY = os.environ.get("KK_API_KEY")
#     FRONT_BASE_URL = "http://127.0.0.1:5500"
#     BACKEND_BASE_URL = "http://127.0.0.1:8000"
#     CORS_ALLOW_ALL_ORIGINS = True
#     CSRF_TRUSTED_ALL_ORIGINS = True
# CORS_ALLOW_CREDENTIALS = True
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.postgres',
    'accounts',
    'community',
    'shortcuts',
    "rest_framework",
    "rest_framework_simplejwt",
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
	'http://localhost:5000',
]

ROOT_URLCONF = 'kikiproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'kikiproject.wsgi.application'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=240),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=2),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
}


AUTH_USER_MODEL = "accounts.User"