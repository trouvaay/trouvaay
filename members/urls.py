from django.conf.urls import patterns, include, url
from members import views


urlpatterns = patterns('',
    url(r'^account/(?P<pk>\d+)$', views.ClosetView.as_view(), name='home'),
)