from django.shortcuts import redirect
import requests
from social.pipeline.partial import partial


@partial
def check_email_presence(backend, details, response, user=None, *args, **kwargs):

    if(user):
        print 'user', user
    if(user and user.email):
        print 'user.email', user.email


    if(user and user.email and '@' in user.email):
        # we have a user and that user has email
        # does not matter what social site returned
        return

    print details
    print response

    if(backend.name == 'facebook'):
        email = response.get('email', None)
        if(not email):

            # we need to revoke the token so that next time during FB login
            # the user is prompted again to give facebook permissions
            fb_token = response.get('access_token', None)
            fb_uid = response.get('id', None)

            print fb_token
            print fb_uid

            if(fb_token and fb_uid):
                url = backend.revoke_token_url(token=response['access_token'], uid=response['id'])
                params = backend.revoke_token_params(token=response['access_token'], uid=response['id'])

                print 'revoking token'
                requests.delete(url, data=params)

            return redirect('members:fb_login_missing_email')
