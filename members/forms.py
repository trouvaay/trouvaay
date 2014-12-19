from django.forms import ModelForm
from members.models import AuthUser
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst

class CustomAuthenticationForm(AuthenticationForm):

	email = forms.EmailField(max_length=254)

	def __init__(self, *args, **kargs):
		super(CustomAuthenticationForm, self).__init__(*args, **kargs)
		del self.fields['username']
		UserModel = get_user_model()
		self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
		if self.fields['email'].label is None:
			self.fields['email'].label = capfirst(self.username_field.verbose_name)


	def clean(self):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')

		if email and password:
			self.user_cache = authenticate(email=email,
		                               password=password)
		if self.user_cache is None:
			raise forms.ValidationError(
				self.error_messages['invalid_login'],
				code='invalid_login',
				params={'email': self.username_field.verbose_name},
			)
		else:
			self.confirm_login_allowed(self.user_cache)

		return self.cleaned_data
