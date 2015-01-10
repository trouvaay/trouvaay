from django.conf.urls import patterns, include, url
from goods import views


urlpatterns = patterns('',
    url(r'^new/$', views.NewView.as_view(), name='new'),
    url(r'^(?P<pk>\d+)/$', views.DetailRouteView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/map/$', views.MapView.as_view(), name='popinmap'),
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^store/(?P<pk>\d+)/$', views.StoreView.as_view(), name='storeprofile'),
    url(r'^vintage/$', views.VintageView.as_view(), name='vintage'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'), 
	url(r'^blog/$', views.BlogView.as_view(), name='blog'),
    url(r'^blog/(?P<pk>\d+)/$', views.BlogPostView.as_view(), name='blogpost'),  
)