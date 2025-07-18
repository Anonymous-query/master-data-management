"""
Django settings for master_data_management project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from common.lib.logsettings import get_logger_config
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PLATFORM_NAME = _('Master Data Management')
PLATFORM_DESCRIPTION = _('MDM is Central Application for all other platforms')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q!j8yjxxd7*o6mapt+e5m9mj16cri2$r6_#ddok#kh63-o5%&u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

############################# SET PATH INFORMATION #############################
PROJECT_ROOT = Path(__file__).resolve().parent.parent 
REPO_ROOT = PROJECT_ROOT.parent
COMMON_ROOT = REPO_ROOT / "common"
ENV_ROOT = REPO_ROOT.parent

MDM_BASE = "localhost:8000"
MDM_ROOT_URL = "http://{}".format(MDM_BASE)

LOGIN_REDIRECT_URL = MDM_ROOT_URL + '/login'
LOGIN_URL = MDM_ROOT_URL + '/login'

# Site info
SITE_NAME = "Master Data Management"
HTTPS = 'on'

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crum',
    'common.mdm_django_utils',
    'common.djangoapps.mdmmako.apps.MDMmakoConfig',
    'common.djangoapps.site_configuration',
    'rest_framework',
    'common.djangoapps.user_authn',
    'common.djangoapps.branding',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'crum.CurrentRequestUserMiddleware',

    # Resets the request cache.
    'common.mdm_django_utils.cache.middleware.RequestCacheMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Enables force_django_cache_miss functionality for TieredCache.
    'common.mdm_django_utils.cache.middleware.TieredCacheMiddleware',

    'common.djangoapps.site_configuration.middleware.SessionCookieDomainOverrideMiddleware',
]

ROOT_URLCONF = 'master_data_management.urls'

################################## TEMPLATE CONFIGURATION #####################################
# Mako templating
import tempfile
MAKO_MODULE_DIR = os.path.join(tempfile.gettempdir(), 'mako_master_data_management')
MAKO_TEMPLATE_DIRS_BASE = [
    os.path.join(PROJECT_ROOT, 'templates'),
    os.path.join(COMMON_ROOT, 'templates'),
    os.path.join(COMMON_ROOT, 'djangoapps/pipeline_mako/templates'),
]

CONTEXT_PROCESSORS = [
    'django.template.context_processors.request',
    'django.template.context_processors.static',
    'django.template.context_processors.i18n',
    'django.contrib.auth.context_processors.auth',  # this is required for admin
    'django.template.context_processors.csrf',

    # Added for django-wiki
    'django.template.context_processors.media',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages',

    'django.template.context_processors.debug',

    'common.djangoapps.site_configuration.context_processors.configuration_context',
]

TEMPLATES = [
    {
        'NAME': 'django',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_ROOT / "templates",
            COMMON_ROOT / 'templates',
            COMMON_ROOT / 'djangoapps' / 'pipeline_mako' / 'templates',
            COMMON_ROOT / 'static',
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'loaders': [
                'common.djangoapps.mdmmako.makoloader.MakoFilesystemLoader',
                'common.djangoapps.mdmmako.makoloader.MakoAppDirectoriesLoader',
            ],
            'context_processors': CONTEXT_PROCESSORS,
        },
    },
    {
        'NAME': 'mako',
        'BACKEND': 'common.djangoapps.mdmmako.backend.Mako',
        'APP_DIRS': False,
        'DIRS': MAKO_TEMPLATE_DIRS_BASE,
        'OPTIONS': {
            'context_processors': CONTEXT_PROCESSORS,
        }
    }
]

WSGI_APPLICATION = 'master_data_management.wsgi.application'
DEFAULT_TEMPLATE_ENGINE = TEMPLATES[0]
DEFAULT_TEMPLATE_ENGINE_DIRS = DEFAULT_TEMPLATE_ENGINE['DIRS'][:]


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
STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = [
    COMMON_ROOT / "static",
    PROJECT_ROOT / "static",
    'static'
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SERVICE_VARIANT = os.environ.get('SERVICE_VARIANT', "master_data_management")

LOGGING_ENV = 'sandbox'
LOCAL_LOGLEVEL = "INFO"
LOG_DIR = f'{os.environ.get("PWD", BASE_DIR)}/var/log/mdm/masterdatamanagement.log'
LOGGING = get_logger_config(LOG_DIR,
                            logging_env=LOGGING_ENV,
                            local_loglevel=LOCAL_LOGLEVEL,
                            service_variant=SERVICE_VARIANT)

LANGUAGE_COOKIE_NAME = "mdm-language-preference"

# Clickjacking protection can be disbaled by setting this to 'ALLOW'
X_FRAME_OPTIONS = 'DENY'

############### Settings for Django Rate limit #####################
RATELIMIT_ENABLE = True

RATELIMIT_RATE = '120/m'

##### LOGISTRATION RATE LIMIT SETTINGS #####
LOGISTRATION_RATELIMIT_RATE = '100/5m'
LOGISTRATION_PER_EMAIL_RATELIMIT_RATE = '30/5m'
LOGISTRATION_PER_USERNAME_RATELIMIT_RATE = '30/5m'
LOGISTRATION_API_RATELIMIT = '20/m'
LOGIN_AND_REGISTER_FORM_RATELIMIT = '100/5m'
# RESET_PASSWORD_TOKEN_VALIDATE_API_RATELIMIT = '30/7d'
# RESET_PASSWORD_API_RATELIMIT = '30/7d'

SHARED_COOKIE_DOMAIN = ''