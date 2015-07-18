from django.conf.urls import patterns, include, url
from django.contrib import admin
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'online_gobang.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url("", include('django_socketio.urls')),
    url(r'^gobang/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/gsl/PycharmProjects/online_gobang/static'}),
    url(r'^gobang/', include('gobang.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/gsl/PycharmProjects/online_gobang/static'}),
)