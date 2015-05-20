from members.models import Join
from django.http import HttpResponsePermanentRedirect
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class ReferralMiddleware():
	def process_request(self, request):
		ref_id = request.GET.get("ref")
		try:
			friend_obj = Join.objects.get(ref_id=ref_id)
		except:
			friend_obj = None
		if friend_obj:
			request.session['join_id_ref'] = friend_obj.id

class WWWRedirectMiddleware(object):
    def process_request(self, request):
        current_request = request.META['HTTP_HOST']
        if current_request.startswith('www.'):
            logger.debug('this is the current request: {}'.formate(current_request))
            return HttpResponsePermanentRedirect(current_request[4:])


