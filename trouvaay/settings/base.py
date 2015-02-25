"""
Django settings for trouvaay project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sslify
from decimal import Decimal

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''
GOOG_MAP_KEY = ''
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [ ]

# works with sslify to force https on Heroku


INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'registration',
    'localflavor',
    'merchants',
    'members',
    'goods',
    'cloudinary',
    # 'debug_toolbar',
    'crispy_forms',
    'stripe',
    'analytical',
    'endless_pagination',
    'social.apps.django_app.default',
)

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.ReferralMiddleware',
)

ROOT_URLCONF = 'trouvaay.urls'

WSGI_APPLICATION = 'trouvaay.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'context_processors.get_liked_items',
    'context_processors.site_name',
    'context_processors.get_feature_context',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'members.AuthUser'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static_prod')
STATIC_URL = '/static/'
# Additional locations of static files`
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
GMAIL_EMAIL =''
GMAIL_PASSWORD = ''
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_FAIL_SILENTLY = not DEBUG

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

FEATURE_NAME_RESERVE = "Reserve"
FEATURE_TOOLTIP_RESERVE = "You'll have 2 days to hold this item and see it in-store. 3 reservation limit"
RETURN_POLICY = {
    'allowed' : '15 day, no hassle return policy. Payment in the form of store credit only.',
    'not_allowed' : 'Sorry, there are no returns on this item. Please email us if you have any specific questions about the product.'
}
SIGNUP_OFFER = "10% off your first purchase after signup"
SITE_ID = 1
SITE_NAME = 'Rare Door'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'raredoor-django.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django.db': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level':'INFO',
        },
        'goods': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'members': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'merchants': {
            'handlers': ['console', 'file'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

# registration settings
ACCOUNT_ACTIVATION_DAYS = 30
REGISTRATION_AUTO_LOGIN = True

STRIPE_CAPTURE_TRANSACTION_TIME = 48  # hours

STRIPE_SECRET_KEY = ''
STRIPE_PUBLISHABLE_KEY = ''
# OLARK_SITE_ID = ''
MIXPANEL_API_TOKEN = ''
ANALYTICAL_INTERNAL_IPS = []

SALES_TAX = Decimal('0.0875')

OFFER_MODAL_EXPIRATION = 3600  # do not show promo offers again whithin this many seconds

RESERVATION_LIMIT = 3  # user cannot have more than this many outstanding reservations

# referral settings
SHARE_URL = ''
ENABLE_REFERRAL = False
LIMIT_REFERRAL_PER_CLIENT_ID = 3
FIRST_REFERRAL_MODAL_EXP = 86400  # do not show first referral modal again within this many seconds, 86400 seconds is 1 day
SECOND_REFERRAL_MODAL_EXP = 86400  # do not show second referral modal again within this many seconds

# email settings are another good candidate to have
# each developer define in their own dev_settings.py
# here are what could be production settings
DEFAULT_FROM_EMAIL = ''  # e.g. 'support@raredoor.com'
EMAIL_HOST = ''  # 'smtp.gmail.com'
EMAIL_PORT = ''  # 587 - for gmail
EMAIL_HOST_USER = ''  # e.g. 'support@raredoor.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True  # google requires True

# social login
SOCIAL_AUTH_FACEBOOK_KEY = '380931628745745'
SOCIAL_AUTH_FACEBOOK_SECRET = '5f84a4d1c72e2962331fb358d3685572'
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['email', 'first_name', 'last_name']
SOCIAL_AUTH_LOGIN_URL = LOGIN_URL
SOCIAL_AUTH_LOGIN_ERROR_URL = LOGIN_URL
SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',

    # this is the default that's why we didn't have it before
    # now that we are explicitly defining AUTHENTICATION_BACKENDS
    # we have to list the default one here as well
    'django.contrib.auth.backends.ModelBackend',
)

PROJECT_ENV = os.getenv('PROJECT_ENV', None)
if(PROJECT_ENV == 'dev'):
    # each developer will have their own dev_settings.py which is in .gitignore
    # this way we won't overwrite each other local settings
    # dev_settings.py will contain for example STRIPE_SECRET_KEY and DATABASES
    from dev_settings import *
