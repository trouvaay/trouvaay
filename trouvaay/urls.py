from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from members import forms
from members.views import SignupView
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy
from registration.backends.default import urls
from registration import auth_urls

urlpatterns = patterns('',

    # here users enter an email address to initiate password reset
    url(r'^accounts/password/reset/$',
        auth_views.password_reset,
       {'post_reset_redirect': reverse_lazy('auth_password_reset_done'),
        'password_reset_form': forms.CustomPasswordResetForm},
       name='auth_password_reset'),
                       
    # here user can enter new password  without providing and old one
    url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'post_reset_redirect': reverse_lazy('auth_password_reset_complete'),
         'set_password_form': forms.CustomSetPasswordForm},
        name='auth_password_reset_confirm'),
              
    url(r'^', include('goods.urls', namespace='goods')),
    url(r'^', include('members.urls', namespace='members')),
    
    url(r'accounts/register/$', SignupView.as_view(), name='registration_register'),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
