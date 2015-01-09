from django.conf.urls import patterns, include, url
from carts import views


urlpatterns = patterns('',
    url(r'^cart/$', views.AddCartProduct, name='addtocart'),
)