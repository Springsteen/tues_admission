from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'campaigns.views.home', name='home'),
    url(r'^campaigns$', 'campaigns.views.list_campaigns', name='list_campaigns'),
    url(r'^campaigns/new$', 'campaigns.views.create_campaign', name='create_campaign'),
    url(r'^campaigns/(\d+)/$', 'campaigns.views.show_campaign', name='show_campaign'),
    url(r'^campaigns/(\d+)/students/new$', 'campaigns.views.create_student', name='create_student'),
    url(r'^admin/', include(admin.site.urls)),
)
