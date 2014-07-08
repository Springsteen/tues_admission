from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'campaigns.views.home', name='home'),
    url(r'^campaigns/new$', 'campaigns.views.create_campaign', name='create_campaign'),
    url(r'^admin/', include(admin.site.urls)),
)
