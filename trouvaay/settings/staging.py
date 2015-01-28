from .base import *
import os

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']
# DEBUG = False
STATIC_ROOT = 'staticfiles'

SECRET_KEY = os.getenv('SECRET_KEY', None)
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', None)
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', None)

ANALYTICAL_INTERNAL_IPS('ANALYTICAL_INTERNAL_IPS', None)
OLARK_SITE_ID = os.getenv('OLARK_SITE_ID', None)
MIXPANEL_API_TOKEN = os.getenv('MIXPANEL_API_TOKEN', None)

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', None)
EMAIL_HOST = os.getenv('EMAIL_HOST', None)  # 'smtp.gmail.com'
EMAIL_PORT = os.getenv('EMAIL_PORT', None)  # 587 - for gmail
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', None)  # e.g. 'support@raredoor.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', None)
ADMINS = os.getenv('ADMINS', None)
