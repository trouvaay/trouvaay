#!/usr/bin/python
from members.models import AuthUserActivity
from django.conf import settings


def get_liked_items(request):
    """ Creates list of user's liked items for json
    Obj passed to addlikehearts js script
    """
    user = request.user
    
    if(not user.is_authenticated()):
        return []

    useractivity, new = AuthUserActivity.objects.get_or_create(authuser=user)
    if new:
        useractivity.save()
    liked_list = useractivity.saved_items.all()
    liked_ids = [prod.id for prod in liked_list]
    return {'liked_items': liked_ids}

def site_name(request):
    return {'site_name': settings.SITE_NAME}

def get_feature_context(request):
    return {
        'FEATURE_NAME_RESERVE': settings.FEATURE_NAME_RESERVE,
        'FEATURE_TOOLTIP_RESERVE': settings.FEATURE_TOOLTIP_RESERVE,
        'FEATURE_TOOLTIP_REVEAL': settings.FEATURE_TOOLTIP_REVEAL,
        'FEATURE_TOOLTIP_OFFER': settings.FEATURE_TOOLTIP_OFFER,
        'TOOLTIP_HEART': settings.TOOLTIP_HEART,
        'TOOLTIP_PURCHASE': settings.TOOLTIP_PURCHASE,
    }
