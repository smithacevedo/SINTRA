# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from decouple import config
from unipath import Path
import platform

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_1122')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# load production server from .env
ALLOWED_HOSTS = ['localhost', '127.0.0.1', config('SERVER', default='127.0.0.1')]

# Todos los proyecto usen BigAutoField por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
    'apps.home',
    'apps.productos',
    'apps.clientes',
    'cities_light',
    'apps.ordenes_compra',
    'apps.proveedores',
    'apps.despachos',
    'apps.remisiones',
    'apps.permisos',
    'apps.roles',
    'apps.usuarios',
    'apps.proyectos',
    #'apps.detalles_orden',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.usuarios.middleware.PrimerAccesoMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.utils.context_processors.permisos_usuario',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sintra',
        'USER': 'postgres',
       'PASSWORD': 'D3v3l0pm3nt',
       # 'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': 5432
    },
}

# Ruta al ejecutable wkhtmltopdf (SE DEBE MODIFICAR CUANDO SE DESPLIEGUE)
# Buscamos primero una copia incluida en la carpeta `core/wkhtmltopdf` (útil en desarrollo):

def _wkhtmltopdf_path():

    # 1) La copia local dentro del mismo directorio `core` (donde está este settings.py)
    core_dir = os.path.dirname(os.path.abspath(__file__))
    system = platform.system()
    candidates = []
    if system == 'Windows':
        candidates = [
            os.path.join(core_dir, 'wkhtmltopdf', 'bin', 'wkhtmltopdf.exe'),
            os.path.join(core_dir, 'wkhtmltopdf', 'wkhtmltopdf.exe'),
        ]
    else:
        candidates = [
            os.path.join(core_dir, 'wkhtmltopdf', 'bin', 'wkhtmltopdf'),
            os.path.join(core_dir, 'wkhtmltopdf', 'wkhtmltopdf'),
        ]

    for p in candidates:
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p


WKHTMLTOPDF_CMD = _wkhtmltopdf_path()

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'apps/static'),
)


#############################################################
# Cities Light settings
CITIES_LIGHT_TRANSLATION_LANGUAGES = ['es']  # Idioma de las ciudades
CITIES_LIGHT_INCLUDE_COUNTRIES = ['CO']  # Solo cargar ciudades de Colombia
#############################################################
