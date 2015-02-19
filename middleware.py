from members.models import Join


class ReferralMiddleware():
	def process_request(self, request):
		ref_id = request.GET.get("ref")
		try:
			friend_obj = Join.objects.get(ref_id=ref_id)
		except:
			friend_obj = None
		if friend_obj:
			request.session['join_id_ref'] = friend_obj.id
