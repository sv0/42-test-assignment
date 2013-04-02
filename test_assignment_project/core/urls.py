from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('test_assignment_project.core.views',
    url(r'^$', 'home', name='home'),
    url(r'^first-requests$', 'first_requests', name='first_requests'),
    #url(r'^edit-contacts$', 'edit_contacts', name='edit_contacts'),
)
