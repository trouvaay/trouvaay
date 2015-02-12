"""
Created on Feb 6, 2015

@author: sergey@lanasoft.net
"""

import os


EXISTING_USER_EMAIL = ''  # test@gmail.com
EXISTING_USER_EMAIL_PASSWORD = ''  # password for email, e.g. for gmail
EXISTING_USER_PASSWORD = ''  # password for the site

# should be a gmail address
# if base email is: example@gmail.com
# when new user is created we will use example+<TIMESTAMP>@gmail.com
# e.g. example+test20150201@gmail.com
NEW_USER_BASE_EMAIL = 'example@gmail.com'

HOME_URL = "http://127.0.0.1:8000/"

NEW_USER_SHIPPING_NAME = 'test'
NEW_USER_SHIPPING_STREET = '123 street'
NEW_USER_SHIPPING_ZIP = '32224'
NEW_USER_CC_NUMBER = '4242424242424242'
NEW_USER_CC_EXP = '1020'
NEW_USER_CC_CSC = '123'


PROJECT_ENV = os.getenv('PROJECT_ENV', None)
if(PROJECT_ENV == 'dev'):
    # each developer will have their own dev_config.py which is in .gitignore
    # this way we won't overwrite each other test configuration settings
    from dev_config import *
