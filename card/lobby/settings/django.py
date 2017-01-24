# Django settings for lobby project.

import os
import djcelery

DEBUG = True
TEMPLATE_DEBUG = DEBUG

LOBBY = os.path.realpath(os.path.join(__file__, os.path.pardir, os.path.pardir))

djcelery.setup_loader()

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('haibin', 'haibin@holytreetech.com'),
    ('jian', 'jian@holytreetech.com'),
)
#EMAIL_USE_SSL = True
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'holytree.logger@gmail.com'
EMAIL_HOST_PASSWORD = 'logger.pwd@gmail'
SERVER_EMAIL = EMAIL_HOST_USER

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'card',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'holytreetech.com',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'card.logger': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'card_logger',
        'USER': 'root',
        'PASSWORD': 'holytreetech.com',
        'HOST': '',
        'PORT': '',
    },
}

DATABASE_ROUTERS = ['card.lobby.router.Router',]  

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Chongqing'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-CN'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(os.path.join(LOBBY, 'static')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!)np4_1&amp;l$nn&amp;*$n4nvg1p2^n_8+3y*9iczodq5nif#!yr-8iy'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'card.lobby.extensions.middleware.ErrorMiddleware',
    'card.lobby.extensions.middleware.MultipleProxyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'card.lobby.extensions.middleware.DataCompressionMiddleware',
    'card.lobby.extensions.middleware.PreSessionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'card.lobby.extensions.middleware.PostSessionMiddleware',
    'card.lobby.extensions.middleware.CsrfFuckMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'card.lobby.extensions.middleware.RequestSerializationMiddleware',
    'card.lobby.extensions.middleware.ActivityMiddleware',
    'card.lobby.extensions.middleware.DurableCounterMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'card.lobby.extensions.middleware.ServiceMiddleware',
    'card.lobby.extensions.middleware.GeoIpMiddleware',
)

ROOT_URLCONF = 'card.lobby.urls'
URL_VERSION = 'three'
LOGIN_REDIRECT_URL = '/' + URL_VERSION + '/player/profile/'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'card.lobby.uwsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(os.path.join(LOBBY, 'apps/holytree/templates')),
    os.path.abspath(os.path.join(LOBBY, 'templates')),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'djcelery',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.admin',
    'rest_framework',
    'card.lobby.apps.player',
    'card.lobby.apps.game',
    'card.lobby.apps.friend',
    'card.lobby.apps.store',
    'card.lobby.apps.rank',
    'card.lobby.apps.holytree',
    'card.lobby.apps.freebie',
    'card.lobby.apps.skypay',
    'card.lobby.apps.turner',
    'card.lobby.apps.mobile',
    'card.lobby.apps.iapppay',
    'card.lobby.apps.roulette',
    'card.lobby.apps.lottery',
    'card.lobby.apps.baidu',
    'card.lobby.apps.zhuoyi',
    'card.lobby.apps.wiipay',
    'card.lobby.apps.youku',
    'card.lobby.apps.dianyou',
    'card.lobby.apps.yuyang',
    'card.lobby.apps.chubao',
    'card.lobby.apps.moguwan',
    'card.lobby.apps.coolpad',
    'card.lobby.apps.dianxin',
    'card.lobby.apps.appchina',
    'card.lobby.apps.ysdk',
    'card.lobby.apps.huawei',
    'card.lobby.apps.invite',
)

AUTHENTICATION_BACKENDS = (
    #'card.lobby.apps.iapppay.backends.IapppayBackend',
    #'card.lobby.apps.baidu.backends.BaiduBackend',
    'card.lobby.apps.moguwan.backends.MoguwanBackend',
    'card.lobby.apps.dianyou.backends.DianyouBackend',
    'card.lobby.apps.yuyang.backends.YuyangBackend',
    'card.lobby.apps.coolpad.backends.CoolpadBackend',
    'card.lobby.apps.ysdk.backends.YsdkBackend',
    'card.lobby.apps.chubao.backends.ChubaoBackend',
    'card.lobby.apps.huawei.backends.HuaweiBackend',
    'django.contrib.auth.backends.ModelBackend',
    'card.lobby.apps.holytree.backends.HolyTreeBackend',
    'card.lobby.apps.holytree.backends.RobotBackend',
    'card.lobby.apps.holytree.backends.GuestBackend',
)

#session cache
from card.lobby.settings.common import CACHE_REDIS
SESSION_ENGINE = 'card.lobby.extensions.session'
SESSION_REDIS_HOST = CACHE_REDIS.host
SESSION_REDIS_PORT = CACHE_REDIS.port
SESSION_REDIS_DB = CACHE_REDIS.db
#SESSION_REDIS_PASSWORD = 'password'
SESSION_REDIS_PREFIX = 'session'
SESSION_MAPPING_KEY = 'session_mapping:{user_id}'

SESSION_COOKIE_AGE=60*60*12 

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%d' % (CACHE_REDIS.host, CACHE_REDIS.port),
        'OPTIONS': {
            'DB': 1,
        },
    },
}

SECURE_PROXY_SSL_HEADER =('HTTP_X_FORWARDED_PROTOCOL','https')
ALLOWED_HOSTS = ['*']
