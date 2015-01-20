from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from members import forms
from members.views import SignupView
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

# from django.contrib.auth import urls
# from django.contrib.auth.views import password_reset

from registration.backends.default import urls
from registration import auth_urls

urlpatterns = patterns('',
                       
   url(r'^accounts/password/reset/$',
       auth_views.password_reset,
       {'post_reset_redirect': reverse_lazy('auth_password_reset_done'),
        'password_reset_form': forms.CustomPasswordResetForm},
       name='auth_password_reset'),
    url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'post_reset_redirect': reverse_lazy('auth_password_reset_complete'),
         'set_password_form': forms.CustomSetPasswordForm},
        name='auth_password_reset_confirm'),
                       
    url(r'^', include('goods.urls', namespace='goods')),
    url(r'^', include('members.urls', namespace='members')),

#    url(r'^password/change/$',
#        auth_views.password_change,
#        {'post_change_redirect': reverse_lazy('auth_password_change_done')},
#        name='auth_password_change'),
#    url(r'^password/change/done/$',
#        auth_views.password_change_done,
#        name='auth_password_change_done'),
   

#    url(r'^password/reset/complete/$',
#        auth_views.password_reset_complete,
#        name='auth_password_reset_complete'),
#    url(r'^password/reset/done/$',
#        auth_views.password_reset_done,
#        name='auth_password_reset_done'),
    

#     url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
#     url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
#         'django.contrib.auth.views.password_reset_confirm',
#         name='password_reset_confirm'),
#     url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

    url(r'accounts/register/$', SignupView.as_view(), name='registration_register'),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
