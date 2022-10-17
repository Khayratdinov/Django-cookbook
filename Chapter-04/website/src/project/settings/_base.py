"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
import json
import sys

from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

from project.apps.core.versioning import get_git_changeset_timestamp


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXTERNAL_BASE = os.path.join(BASE_DIR, "externals")
EXTERNAL_LIBS_PATH = os.path.join(EXTERNAL_BASE, "libs")
EXTERNAL_APPS_PATH = os.path.join(EXTERNAL_BASE, "apps")
sys.path = ["", EXTERNAL_LIBS_PATH, EXTERNAL_APPS_PATH] + sys.path


with open(os.path.join(os.path.dirname(__file__), "secrets.json"), "r") as f:
    secrets = json.loads(f.read())


def get_secret(setting):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = f"Set the {setting} secret variable"
        raise ImproperlyConfigured(error_msg)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-j#v+wzwn571o*9!d3w=mhqc_s4uqb=b=8izk=55_wbg#va5qw8'
SECRET_KEY = get_secret("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django.forms",
    "imagekit",
    "crispy_forms",
    "qr_code",
    "django_json_ld",
    "haystack",
    "sekizai",
    "project.apps.core",
    "project.apps.magazine",
    "project.apps.ideas",
    "project.apps.categories",
    "project.apps.search",
    "project.apps.locations",
    "project.apps.likes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


WEBSITE_URL = "http://127.0.0.1:8000"
ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "project", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "project.apps.core.context_processors.website_url",
                "sekizai.context_processors.sekizai",
                "project.apps.core.context_processors.google_maps",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
#     }
# }

# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     'NAME': get_secret('DATABASE_NAME'),
#     'USER': get_secret('DATABASE_USER'),
#     'PASSWORD': get_secret('DATABASE_PASSWORD'),
#     'HOST': 'db',
#     'PORT': '5432',
#   }
# }


DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": get_secret("DATABASE_NAME"),
        "USER": get_secret("DATABASE_USER"),
        "PASSWORD": get_secret("DATABASE_PASSWORD"),
        "HOST": "localhost",
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ("bg", "Bulgarian"),
    ("hr", "Croatian"),
    ("cs", "Czech"),
    ("da", "Danish"),
    ("nl", "Dutch"),
    ("en", "English"),
    ("et", "Estonian"),
    ("fi", "Finnish"),
    ("fr", "French"),
    ("de", "German"),
    ("el", "Greek"),
    ("hu", "Hungarian"),
    ("ga", "Irish"),
    ("it", "Italian"),
    ("lv", "Latvian"),
    ("lt", "Lithuanian"),
    ("mt", "Maltese"),
    ("pl", "Polish"),
    ("pt", "Portuguese"),
    ("ro", "Romanian"),
    ("sk", "Slovak"),
    ("sl", "Slovene"),
    ("es", "Spanish"),
    ("sv", "Swedish"),
    ("uz", "Uzbekistan"),
]

LANGUAGES_EXCEPT_THE_DEFAULT = [
    (lang_code, lang_name)
    for lang_code, lang_name in LANGUAGES
    if lang_code != LANGUAGE_CODE
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

HAYSTACK_CONNECTIONS = {}
for lang_code, lang_name in LANGUAGES:
    lang_code_underscored = lang_code.replace("-", "_")
    HAYSTACK_CONNECTIONS[f"default_{lang_code_underscored}"] = {
        "ENGINE": "project.apps.search.multilingual_whoosh_backend.MultilingualWhooshEngine",
        "PATH": os.path.join(BASE_DIR, "tmp", f"whoosh_index_{lang_code_underscored}"),
    }
lang_code_underscored = LANGUAGE_CODE.replace("-", "_")
HAYSTACK_CONNECTIONS["default"] = HAYSTACK_CONNECTIONS[
    f"default_{lang_code_underscored}"
]

COUNTRY_CHOICES = [
    ("BE", _("Belgium")),
    ("BG", _("Bulgaria")),
    ("CZ", _("Czechia")),
    ("DK", _("Denmark")),
    ("DE", _("Germany")),
    ("EE", _("Estonia")),
    ("IE", _("Ireland")),
    ("EL", _("Greece")),
    ("ES", _("Spain")),
    ("FR", _("France")),
    ("HR", _("Croatia")),
    ("IT", _("Italy")),
    ("CY", _("Cyprus")),
    ("LV", _("Latvia")),
    ("LT", _("Lithuania")),
    ("LU", _("Luxembourg")),
    ("HU", _("Hungary")),
    ("MT", _("Malta")),
    ("NL", _("Netherlands")),
    ("AT", _("Austria")),
    ("PL", _("Poland")),
    ("PT", _("Portugal")),
    ("RO", _("Romania")),
    ("SI", _("Slovenia")),
    ("SK", _("Slovakia")),
    ("FI", _("Finland")),
    ("SE", _("Sweden")),
    ("UK", _("United Kingdom")),
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# with open(os.path.join(BASE_DIR, 'project', 'settings', 'last-modified.txt'), 'r') as f:
#   timestamp = f.readline().strip()

STATICFILES_DIRS = [os.path.join(BASE_DIR, "project", "site_static")]

timestamp = get_git_changeset_timestamp(BASE_DIR)
STATIC_URL = f"/static/{timestamp}/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# STATIC_URL = '/static/'
# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [STATIC_DIR]
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


MAGAZINE_ARTICLE_THEME_CHOICES = [
    ("futurism", _("Futurism")),
    ("nostalgia", _("Nostalgia")),
    ("sustainability", _("Sustainability")),
    ("wonder", _("Wonder")),
    ("positivity", _("Positivity")),
    ("solutions", _("Solutions")),
    ("science", _("Science")),
]

CRISPY_TEMPLATE_PACK = "bootstrap4"
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

GOOGLE_MAPS_API_KEY = get_secret("GOOGLE_MAPS_API_KEY")
