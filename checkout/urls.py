from django.conf.urls import patterns, include, url
from checkout import views


urlpatterns = patterns('',
    url(r'^stripe/$', views.StripeView.as_view(), name='stripe'),
)