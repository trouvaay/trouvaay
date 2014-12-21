from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'trouvaay.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^', include('goods.urls', namespace='goods')),
    url(r'^', include('members.urls', namespace='members')),
    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
