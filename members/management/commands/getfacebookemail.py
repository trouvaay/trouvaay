"""
Created on Apr 28, 2015

@author: sergey@lanasoft.net
"""


from django.core.management.base import BaseCommand
from social.apps.django_app.default.models import UserSocialAuth
from social.apps.django_app.utils import load_strategy, load_backend

from members.models import AuthUser


def get_facebook_email(user):
    """Returns user email from Facebook
    This would only work if both of the following are true:
    1. There is a mapping between user and facebook user
    that is if this user has loggined/signed up via facebook
    2. The access token for this user is still valid
    """

    if(hasattr(user, 'social_auth')):
        social_auth = user.social_auth.first()
        if(hasattr(social_auth, 'extra_data') and social_auth.extra_data):

            extra_data = social_auth.extra_data
            fb_token = extra_data.get('access_token', None)
            fb_uid = extra_data.get('id', None)

            if(fb_token and fb_uid):
                
                strategy = load_strategy()
                backend = load_backend(strategy=strategy, name='facebook', redirect_uri=None)

                try:
                    data = backend.user_data(access_token=fb_token)
                    if(data and isinstance(data, dict)):
                        email = data.get('email', None)
                        # if (not email):
                        #     raise Exception('No email present in facebook email data')
                        # else:
                        if(email and '@' in email):
                            return email
                except Exception, e:
                    if('400 Client Error' in str(e)):
                        # this is most likely bad access_token, nothing we can do
                        print 'cannot get facebook email for user id', user.id, 'probably an invalid access_token'
                        pass
                    else:
                        raise

    return None

def count_users_without_email():
    """Returns the number of users who do not have proper email in database"""

    result = 0
    
    users = AuthUser.objects.all().order_by('id')
    for user in users:
        if(not user.email or '@' not in user.email):
            print 'user', user.id, 'needs to update email from facebook'
            result += 1
    return result

class Command(BaseCommand):
    help = 'Retrieves email from Facebook and saves it in database for users who signed up via Facebook but are missing email'

    def handle(self, *args, **options):

        count_skipped_users = 0
        count_updated_emails = 0
        count_missing_emails = count_users_without_email()
        print 'there are {0} users who are missing emails'.format(count_missing_emails)
        print

        fb_users = UserSocialAuth.objects.all()
        for fb_user in fb_users:
            user = fb_user.user

            if(not user.email or '@' not in user.email):
                # user is missing email
                
                print 'getting email for {}'.format(user.email.encode('utf-8').strip())

                email = get_facebook_email(user)
                if(email):
                    old_email = user.email

                    try:
                        existing_user = AuthUser.objects.get(email=email)
                        print 'cannot set email to', email, 'for user id', user.id, 'because there is already another user', existing_user.id, 'with such email'
                        count_skipped_users += 1

                    except AuthUser.DoesNotExist:
                        # this is what we want
                        user.email = email
                        user.save()

                        print 'updated user id', user.id, 'old email', old_email, 'new email', user.email
                        count_updated_emails += 1

        count_missing_emails = count_users_without_email()

        print
        print 'skipped users', count_skipped_users
        print 'updated emails', count_updated_emails
        print 'there are {0} users who are still missing emails'.format(count_missing_emails)
