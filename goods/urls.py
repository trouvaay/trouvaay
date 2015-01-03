from django.conf.urls import patterns, include, url
from goods import views


urlpatterns = patterns('',
    url(r'^$', views.HomeView.as_view(), name='new'),
    url(r'^(?P<pk>\d+)/$', views.DetailRouteView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/map/$', views.MapView.as_view(), name='popinmap'),
    url(r'^nearby/$', views.NearbyView.as_view(), name='nearby'),
    url(r'^store/(?P<pk>\d+)/$', views.StoreView.as_view(), name='storeprofile'),  
)