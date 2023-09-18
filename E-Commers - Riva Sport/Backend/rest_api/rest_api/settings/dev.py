from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'development-secret'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','127.0.0.1', '::1']

# Application definition

DJANGO_APP = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MY_APP = [
    'riva_api',
    'theme',
]

THIRD_PARTY_PACKAGES = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_cleanup.apps.CleanupConfig',

    "django_browser_reload",
    'tailwind',
]

INSTALLED_APPS = DJANGO_APP + MY_APP + THIRD_PARTY_PACKAGES

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

# ketika menggunakan postgresql harus install "psycopg"
# pip3 install psycopg

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'api',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

TAILWIND_APP_NAME = 'theme'