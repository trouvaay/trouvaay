from django.conf.urls import patterns, include, url
from goods import views


urlpatterns = patterns('',
    url(r'^$', views.LandingView.as_view(), name='landing'),
    url(r'^shop/$', views.ShopView.as_view(), name='shop'),
    url(r'^piece/(?P<slug>[-\w\d]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^returns/$', views.ReturnsView.as_view(), name='returns'),
    url(r'^searchfilter/$', views.SearchFilterView.as_view(), name='searchfilter'),

    #TODO: add unique url generator for vintage sales from IG
    #url(r'^vintage/$', views.VintageView.as_view(), name='vintage'),

    # Additional copy pages
    # url(r'^(?P<pk>\d+)/map/$', views.DirectionsView.as_view(), name='popinmap'),
    # url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    # url(r'^blog/$', views.BlogView.as_view(), name='blog'),
    # url(r'^blog/post/(?P<pk>\d+)/$', views.BlogPostView.as_view(), name='blogpost'),
)
