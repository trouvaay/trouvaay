from django.shortcuts import render
from django.views import generic
from members.models import AuthUserActivity, AuthUser
from members.forms import CustomAuthenticationForm
from django.contrib.auth import views

class ClosetView(generic.ListView):
	template_name = 'members/closet/closet.html'
	context_object_name = 'saved_items'
	model = AuthUserActivity

class SignupView(generic.FormView):
	template_name = 'members/auth/signup.html'
	model = AuthUser
	form_class = CustomAuthenticationForm

	def post(self, request, *args, **kwargs):
	    form_class = self.get_form_class()
	    form = self.get_form(form_class)
	    if form.is_valid():
	        return self.form_valid(form)
	    else:
	        return self.form_invalid(form)

class SignupView(generic.CreateView):
	template_name = 'members/auth/signup.html'
	model = AuthUser
	form_class = CustomAuthenticationForm