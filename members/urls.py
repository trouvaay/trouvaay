from django.conf.urls import patterns, include, url
from members import views
from members.forms import CustomAuthenticationForm


urlpatterns = patterns('',
    url(r'^account/(?P<pk>\d+)$', views.ClosetView.as_view(), name='closet'),
    url(r'^login/$', 'django.contrib.auth.views.login', 
    	{'template_name': 'members/auth/login.html', 'authentication_form' : CustomAuthenticationForm}, name='login'),
)