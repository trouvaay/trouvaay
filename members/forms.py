from django.forms import ModelForm
from members.models import AuthUser, Join
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, \
    SetPasswordForm
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit, Div, Button, HTML
from localflavor.us.forms import USPhoneNumberField
import logging

logger = logging.getLogger(__name__)

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_show_errors = True
        self.helper.form_method = 'post'
#       self.helper.form_action = 'auth_password_reset'
        self.helper.form_id = 'form-reset-password'

        self.helper.layout = Layout(
            Fieldset(
                'Enter your new password below to reset your password:',
                Div(
                    Field('new_password1', placeholder='New password'),
                    Field('new_password2', placeholder='New password Confirmation'),
                    Submit('button-reset-password', 'Set password', css_class="btn-primary"),
                    css_class='col-xs-10 col-xs-offset-1'
                )
            ),
        )

    class Meta:
        fields = ('new_password1', 'new_password2')

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_show_errors = True
        self.helper.form_method = 'post'
        self.helper.form_action = 'auth_password_reset'
        self.helper.form_id = 'form-reset-password'

        self.helper.layout = Layout(
            Fieldset(
                'Forgot your password?',
                Div(
                    HTML("Enter your email in the form below and we'll send you instructions for creating a new one."),
                    Field('email', placeholder='Email address'),
                    Submit('button-reset-password', 'Reset password', css_class="btn-primary"),
                    css_class='col-xs-10 col-xs-offset-1'
                )
            ),
        )

    class Meta:
        fields = ('email',)

class CustomAuthenticationForm(AuthenticationForm):
    # TODO: add "next" hidden field
    email = forms.EmailField(max_length=254)
    next = forms.CharField(max_length=1000, required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kargs)
        del self.fields['username']
        self.fields['password'].widget.attrs['placeholder'] = 'password'

        # Adding classes to fields
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'

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
                Field('next'),
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

class ReserveFormAuth(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput, required=True)
    last_name = forms.CharField(widget=forms.TextInput, required=True)
    phone = USPhoneNumberField(required=True)

    def __init__(self, *args, **kwargs):
        super(ReserveFormAuth, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_show_errors = True
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.form_id = 'form-reserve'

        self.helper.layout = Layout(
            Field('first_name', placeholder='First name'),
            Field('last_name', placeholder='Last name'),
            Field('phone', placeholder='Phone number'),
            Button('button-reserve', 'Submit', css_class="btn-success"),
        )

class ReserveForm(ReserveFormAuth):
    email = forms.EmailField(widget=forms.TextInput, required=True)

    def __init__(self, *args, **kwargs):
        super(ReserveForm, self).__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Field('first_name', placeholder='First name'),
            Field('last_name', placeholder='Last name'),
            Field('email', placeholder='Email address'),
            Field('phone', placeholder='Phone number'),
            Button('button-reserve', 'Submit', css_class="btn-success"),
        )

class PostCheckoutForm(forms.Form):
    email = forms.CharField(widget=forms.HiddenInput)
    post_checkout_hash = forms.CharField(widget=forms.HiddenInput)
    phone = USPhoneNumberField(required=True)

    def __init__(self, *args, **kwargs):
        super(PostCheckoutForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_show_errors = True
        self.helper.form_method = 'post'
        self.helper.form_action = 'members:post_checkout_update'
        self.helper.form_id = 'form-post-checkout'

        self.helper.layout = Layout(
            Field('email'),
            Field('post_checkout_hash'),
            Field('phone', placeholder='Phone number'),
            Button('post-checkout', 'Submit', css_class="btn-success"),
        )

# class ReserveForm(forms.Form):
#     first_name = forms.CharField(widget=forms.TextInput, required=True)
#     last_name = forms.CharField(widget=forms.TextInput, required=True)
#     email = forms.EmailField(widget=forms.TextInput, required=True)
#     phone = USPhoneNumberField(required=True)
#
#     def __init__(self, *args, **kwargs):
#         super(ReserveForm, self).__init__(*args, **kwargs)
#
#         self.helper = FormHelper()
#         self.helper.form_show_labels = False
#         self.helper.form_show_errors = True
#         self.helper.form_method = 'post'
#         self.helper.form_action = '.'
#         self.helper.form_id = 'form-reserve'
#
#         self.helper.layout = Layout(
#             Field('first_name', placeholder='First name'),
#             Field('last_name', placeholder='Last name'),
#             Field('email', placeholder='Email address'),
#             Field('phone', placeholder='Phone number'),
#             Button('button-reserve', 'Submit', css_class="btn-success"),
#         )



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
        password2 = cleaned_data.get("password2")

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


class ReferralForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput, required=True)

    def __init__(self, *args, **kwargs):
        super(ReferralForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.form_show_errors = True
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.form_id = 'form-referral'

        self.helper.layout = Layout(
            Field('email', placeholder='Email address'),
            Submit('button-signup', 'Submit', css_class="btn-success"),
        )

