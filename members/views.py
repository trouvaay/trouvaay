from django.shortcuts import render
from django.views import generic
from members.models import AuthUserActivity


class ClosetView(generic.ListView):
	template_name = 'members/closet/closet.html'
	context_object_name = 'saved_items'
	model = AuthUserActivity
