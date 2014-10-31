from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'campaigns.views.home', name='home'),
    url(r'^logout$', 'campaigns.views.logout_user', name='logout_user'),
    url(r'^campaigns$', 'campaigns.views.list_campaigns', name='list_campaigns'),
    url(r'^campaigns/new$', 'campaigns.views.create_campaign', name='create_campaign'),
    url(r'^campaigns/(\d+)/$', 'campaigns.views.show_campaign', name='show_campaign'),
    url(r'^campaigns/(\d+)/delete$', 'campaigns.views.delete_campaign', name='delete_campaign'),
    url(r'^campaigns/(\d+)/search$', 'campaigns.views.search_campaign', name='search_campaign'),
    url(r'^campaigns/(\d+)/halls$', 'campaigns.views.populate_halls', name='populate_halls'),
    url(r'^campaigns/(\d+)/halls/new$', 'campaigns.views.create_hall', name='create_hall'),
    url(r'^campaigns/(\d+)/halls/(\d+)$/delete', 'campaigns.views.delete_hall', name='delete_hall'),
    url(r'^campaigns/(\d+).csv/$', 'campaigns.views.export_as_csv', name='export_as_csv'),
    url(r'^campaigns/(\d+)/students/new$', 'campaigns.views.create_student', name='create_student'),
    url(r'^campaigns/(\d+)/students/(\d+)/$', 'campaigns.views.show_student', name='show_student'),
    url(r'^campaigns/(\d+)/students/(\d+).pdf/$', 'campaigns.views.student_as_pdf', name='student_as_pdf'),
    url(r'^campaigns/(\d+)/students/(\d+)/edit$', 'campaigns.views.edit_student', name='edit_student'),
    url(r'^campaigns/(\d+)/students/(\d+)/delete$', 'campaigns.views.delete_student', name='delete_student'),
    url(r'^admin/', include(admin.site.urls)),
)
