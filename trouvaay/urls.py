from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from members.views import SignupView


urlpatterns = patterns('',
    url(r'^', include('goods.urls', namespace='goods')),
    url(r'^', include('members.urls', namespace='members')),
    url(r'accounts/register/$', SignupView.as_view(), name='registration_register'),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
