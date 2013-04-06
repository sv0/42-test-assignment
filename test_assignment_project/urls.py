from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'test_assignment_project.core.views.home', name='home'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^core/', include('test_assignment_project.core.urls')),
    url(r'^admin/', include(admin.site.urls)),

)
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
