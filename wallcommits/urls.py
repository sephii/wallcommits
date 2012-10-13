from django.conf.urls import patterns, include, url
from django.views.generic import ListView
from flickr.models import Photo

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(
        queryset=Photo.objects.all()[:50]
    ), name='home'),
    url(r'^flickr/', include('flickr.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
