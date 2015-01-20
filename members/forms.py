from django.forms import ModelForm
from members.models import AuthUser
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit, Div, Button

class CustomPasswordResetForm(PasswordResetForm):
	def __init__(self, *args, **kargs):
		super(CustomPasswordResetForm, self).__init__(*args, **kargs)
		
		self.helper = FormHelper()
		self.helper.form_show_labels = False
		self.helper.form_show_errors = True
		self.helper.form_method = 'post'
		self.helper.form_action = 'password_reset'
		self.helper.form_id = 'form-reset-password'

		self.helper.layout = Layout(
			Fieldset(
				'Forgot your password?',
				Div("Enter your email in the form below and we'll send you instructions for creating a new one."),
				Field('email', placeholder='Email address'),
				Submit('button-reset-password', 'Reset password', css_class="btn-primary"),
			),
		)
		
	class Meta:
		fields = ('email',)

class CustomAuthenticationForm(AuthenticationForm):

	email = forms.EmailField(max_length=254)

	def __init__(self, *args, **kargs):
		super(CustomAuthenticationForm, self).__init__(*args, **kargs)
		del self.fields['username']
		self.fields['password'].widget.attrs['placeholder'] = 'password'
		UserModel = get_user_model()
		self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
		if self.fields['email'].label is None:
			self.fields['email'].label = capfirst(self.username_field.verbose_name)

		self.helper = FormHelper()
		self.helper.form_show_labels = False
		self.helper.form_show_errors = True
		self.helper.form_method = 'post'
		self.helper.form_action = 'members:login'
		self.helper.form_id = 'form-login'

		self.helper.layout = Layout(
			Fieldset(
				'Already a member? Log in',
				Field('email', placeholder='Email address'),
				Field('password', placeholder='Password'),
				Submit('button-login', 'Step Inside', css_class="btn-default"),
			),
								
		)

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

class RegistrationForm(forms.ModelForm):

	email = forms.EmailField(widget=forms.TextInput, required=True)
	password = forms.CharField(widget=forms.PasswordInput, required=True)
	password2 = forms.CharField(widget=forms.PasswordInput, required=True)

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper()
		self.helper.form_show_labels = False
		self.helper.form_show_errors = True
		self.helper.form_method = 'post'
		self.helper.form_action = 'registration_register'
		self.helper.form_id = 'form-signup'

		self.helper.layout = Layout(
			Fieldset(
				'Create an account',
				Field('email', placeholder='Email address'),
				Field('password', placeholder='Password'),
				Field('password2', placeholder='Confirm Password'),
				Submit('submit', 'Submit', css_class="btn-primary"),
			),
		)

	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		
		password = cleaned_data.get("password")
		password2 = cleaned_data.get("password")

		if password != password2:
			msg = "Your passwords should match."
			self.add_error('password', msg)
			self.add_error('password2', msg)		
		return cleaned_data

	def save(self, commit=True):

		print 'in form.save()'

		user = super(RegistrationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user

	class Meta:
		model = get_user_model()
		fields = ('email', 'password', 'password2')

