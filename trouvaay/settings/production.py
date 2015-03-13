from .staging import *

DEBUG = False

SHARE_URL = "https://raredoor.com/?ref="
ENABLE_REFERRAL = False
LIMIT_REFERRAL_PER_CLIENT_ID = 3
FIRST_REFERRAL_MODAL_EXP = 86400  # do not show first referral modal again within this many seconds, 86400 seconds is 1 day
SECOND_REFERRAL_MODAL_EXP = 86400
OFFER_MODAL_EXPIRATION = 3600

# social login
ENABLE_SOCIAL_AUTH = True
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
