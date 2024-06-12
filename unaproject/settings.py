from pathlib import Path
from os import getenv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-^5$zyxp&*()5i^57iom_z2-)kcsydd!-2rj=h^q($y_5n@5vaw'

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'unaapp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'unaproject.urls'

WSGI_APPLICATION = 'unaproject.wsgi.application'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': "una_health_db",
            'USER': "una_user",
            'PASSWORD': "secret_password",
            'HOST': getenv('DB_HOST', 'localhost'),
            'PORT': 5432,
        }
    }

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
