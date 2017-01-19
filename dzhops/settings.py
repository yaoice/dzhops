"""
Django settings for dzhops project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from oslo_utils import netutils

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2vuicou20ne9t&h)#c2!7sz4cc+6hcfxfmy!4agjs7@7-$nddq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# cookie timeout
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Application definition

INSTALLED_APPS = (
# pip install django-admin-bootstrapped
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'index',
    'dzhops',
    'hostlist',
    'replacedata',
    'saltstack',
    'record',
    'newtest',
    'templatelibrary',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dzhops.urls'

WSGI_APPLICATION = 'dzhops.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

LOCAL_IP = netutils.get_my_ipv4()

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': LOCAL_IP + ':11211',

    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dzhops',
        'USER': 'dzhops',
        'PORT': 3306,
        'HOST': LOCAL_IP,
        'PASSWORD': 'dzhinternet',
        'default-character-set': 'utf8'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_URL = '/static/'
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# salt-api setting
SALT_API = {
    'url': 'http://' + LOCAL_IP + ':8888/',
    'user': 'saltapi',
    'password': '99cloud'
}

enable_sendEmail = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'openstackxxcloud@163.com'
EMAIL_HOST_PASSWORD = 'openstackxxcloud'
DEFAULT_FROM_EMAIL = 'OpenStack Deploy Robot <openstack99cloud@163.com>'
TO_EMAIL = ['xxx@cloud.net']

# log setting
try:
    from config_log import LOGGING
except:
    pass
