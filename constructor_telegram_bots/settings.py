from django.utils.translation import gettext_lazy as _

import django_stubs_ext

from dotenv import load_dotenv

from datetime import timedelta
from pathlib import Path
from typing import Any, Literal
import os
import secrets
import sys

django_stubs_ext.monkeypatch()
load_dotenv()


BASE_DIR: Path = Path(__file__).resolve().parent.parent

SECRET_KEY: str = os.getenv('SECRET_KEY', secrets.token_hex(25))

DEBUG: bool = os.getenv('DEBUG', 'True') == 'True'
ENABLE_TELEGRAM_AUTH: bool = os.getenv('ENABLE_TELEGRAM_AUTH', 'True') == 'True'

match sys.argv:
	case ['manage.py', 'test', *extra_options]:
		TEST = True
	case __:
		TEST = False

TELEGRAM_BOT_TOKEN: str = os.environ['TELEGRAM_BOT_TOKEN']

FRONTEND_PATH: str = os.environ['FRONTEND_PATH']

POSTGRESQL_DATABASE_NAME: str = os.environ['POSTGRESQL_DATABASE_NAME']
POSTGRESQL_DATABASE_USER: str = os.environ['POSTGRESQL_DATABASE_USER']
POSTGRESQL_DATABASE_PASSWORD: str = os.environ['POSTGRESQL_DATABASE_PASSWORD']


ALLOWED_HOSTS: list[str] = ['*'] if DEBUG else ['constructor.exg1o.org']


CSRF_COOKIE_AGE: int = 2419200  # 4 weeks
SESSION_COOKIE_AGE: int = 2419200  # 4 weeks


JWT_REFRESH_TOKEN_COOKIE_NAME: str = 'jwt_refresh_token'
JWT_ACCESS_TOKEN_COOKIE_NAME: str = 'jwt_access_token'
JWT_REFRESH_TOKEN_LIFETIME: timedelta = timedelta(weeks=4)
JWT_ACCESS_TOKEN_LIFETIME: timedelta = timedelta(minutes=15)
JWT_TOKEN_COOKIE_SECURE: bool = False
JWT_TOKEN_COOKIE_HTTPONLY: bool = True
JWT_TOKEN_COOKIE_SAMESITE: Literal['Lax', 'Strict', 'None'] = 'Lax'


CELERY_BROKER_URL: str = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND: str = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT: list[str] = ['application/json']
CELERY_RESULT_SERIALIZER: str = 'json'
CELERY_TASK_SERIALIZER: str = 'json'
CELERY_BEAT_SCHEDULE: dict[str, dict[str, Any]] = {
	'check_tokens_expiration_date_schedule': {
		'task': 'users.tasks.check_tokens_expiration_date',
		'schedule': 86400,  # 24h
	},
}


INSTALLED_APPS: list[str] = [
	'rest_framework',
	'django_filters',
	'drf_standardized_errors',
	'admin_interface',
	'colorfield',
	'modeltranslation',
	'tinymce',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'languages',
	'users',
	'telegram_bots',
	'telegram_bots.hub',
	'updates',
	'instruction',
	'donation',
	'privacy_policy',
]

if not TEST and DEBUG:
	INSTALLED_APPS.append('silk')

REST_FRAMEWORK: dict[str, Any] = {
	'EXCEPTION_HANDLER': 'drf_standardized_errors.handler.exception_handler'
}

TINYMCE_DEFAULT_CONFIG: dict[str, Any] = {
	'theme': 'silver',
	'menubar': True,
	'height': 420,
	'plugins': (
		'advlist, autolink, lists, link, image, charmap,'
		'print, preview, anchor, searchreplace, visualblocks,'
		'code, fullscreen, insertdatetime, media, table, paste,'
		'help, wordcount'
	),
	'toolbar': (
		'undo redo | '
		'formatselect | '
		'bold italic backcolor | '
		'alignleft aligncenter alignright alignjustify | '
		'bullist numlist outdent indent | '
		'removeformat | '
		'help'
	),
}


MIDDLEWARE: list[str] = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'django.middleware.locale.LocaleMiddleware',
]

if not TEST and DEBUG:
	MIDDLEWARE.append('silk.middleware.SilkyMiddleware')


TEMPLATES: list[dict[str, Any]] = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [FRONTEND_PATH],
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

AUTHENTICATION_BACKENDS: list[str] = ['users.backends.TelegramBackend']

AUTH_USER_MODEL: str = 'users.User'
ROOT_URLCONF: str = 'constructor_telegram_bots.urls'
WSGI_APPLICATION: str = 'constructor_telegram_bots.wsgi.application'


CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.redis.RedisCache',
		'LOCATION': 'redis://127.0.0.1:6379',
	}
}


DATABASES: dict[str, dict[str, Any]] = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': POSTGRESQL_DATABASE_NAME,
		'USER': POSTGRESQL_DATABASE_USER,
		'PASSWORD': POSTGRESQL_DATABASE_PASSWORD,
		'HOST': '127.0.0.1',
		'PORT': '5432',
	},
}
DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'


USE_I18N: bool = True
USE_L10N: bool = True

LANGUAGE_COOKIE_NAME: str = 'lang'

LANGUAGES: list[tuple[str, Any]] = [
	('en', _('Английский')),
	('uk', _('Украинский')),
	('ru', _('Русский')),
]
LANGUAGE_CODE: str = 'ru-ru'
MODELTRANSLATION_DEFAULT_LANGUAGE: str = 'ru'
LOCALE_PATHS: list[Path] = [BASE_DIR / 'locale']


TIME_ZONE: str = 'UTC'
USE_TZ: bool = True


STATIC_URL: str = '/static/'
STATIC_ROOT: Path = BASE_DIR / 'static'
STATICFILES_DIRS: list[Path | str] = [FRONTEND_PATH]

MEDIA_URL: str = '/media/'
MEDIA_ROOT: Path = BASE_DIR / 'media'


os.makedirs(BASE_DIR / 'logs', exist_ok=True)

LOGGING: dict[str, Any] = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'verbose': {
			'format': '[{asctime}]: {levelname}: {name} > {funcName} || {message}',
			'style': '{',
		},
		'simple': {
			'format': '[{asctime}]: {message}',
			'style': '{',
		},
	},
	'handlers': {
		'console': {
			'level': 'INFO',
			'class': 'logging.StreamHandler',
			'formatter': 'simple',
		},
		'django_info_file': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': BASE_DIR / 'logs/django_info.log',
			'maxBytes': 10485760,
			'backupCount': 10,
			'formatter': 'verbose',
		},
		'django_error_file': {
			'level': 'WARNING',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': BASE_DIR / 'logs/django_error.log',
			'maxBytes': 10485760,
			'backupCount': 10,
			'formatter': 'verbose',
		},
	},
	'loggers': {
		'django': {
			'handlers': [
				'console',
				'django_info_file',
				'django_error_file',
			],
			'propagate': True,
		},
	},
}
