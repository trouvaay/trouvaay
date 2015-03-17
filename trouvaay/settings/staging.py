from .base import *
import os

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SSLIFY_DISABLE = False

# Allow all host headers
ALLOWED_HOSTS = ['*']
DEBUG = True
#STATIC_ROOT = 'static'
SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('SOCIAL_AUTH_FACEBOOK_KEY', None)
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('SOCIAL_AUTH_FACEBOOK_SECRET', None)

SHARE_URL = "https://raredoor-staging.herokuapp.com/?ref="
ENABLE_REFERRAL = False
LIMIT_REFERRAL_PER_CLIENT_ID = 10
FIRST_REFERRAL_MODAL_EXP = 1  # do not show first referral modal again within this many seconds, 86400 seconds is 1 day
SECOND_REFERRAL_MODAL_EXP = 1

OFFER_IS_ENABLED = False

OFFER_MODAL_EXPIRATION = 10
CLICK_EXCLUSIONS = ['blakesadams@gmail.com', 'adavis@goturnsile.co', 'and2eyes@gmail.com', 'brennaadams@gmail.com']
SECRET_KEY = os.getenv('SECRET_KEY', None)
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', None)
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', None)
ANALYTICAL_INTERNAL_IPS = ('ANALYTICAL_INTERNAL_IPS', None)
# OLARK_SITE_ID = os.getenv('OLARK_SITE_ID', None)
# MIXPANEL_API_TOKEN = os.getenv('MIXPANEL_API_TOKEN', None)
GMAIL_EMAIL = os.getenv('GMAIL_EMAIL', None)
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD', None)
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', None)
EMAIL_HOST = os.getenv('EMAIL_HOST', None)  # 'smtp.gmail.com'
EMAIL_PORT = os.getenv('EMAIL_PORT', None)  # 587 - for gmail
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', None)  # e.g. 'support@raredoor.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', None)
ADMINS = os.getenv('ADMINS', None)
INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'localflavor',
    'merchants',
    'members',
    'goods',
    'cloudinary',
    'crispy_forms',
    'stripe',
    'registration',
    'analytical',
    'endless_pagination',
    'social.apps.django_app.default',
)
