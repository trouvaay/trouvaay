from django.conf.urls import patterns, include, url
from goods import views


urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.HomeView.as_view(), name='home'),   
)