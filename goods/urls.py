from django.conf.urls import patterns, include, url
from goods import views


urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/map/$', views.MapView.as_view(), name='detail'),  
)