from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from rest_framework.urlpatterns import format_suffix_patterns

from workrave.cloud.redisview import RedisView
from workrave.cloud.views import ConfigurationList, ConfigurationInstance, UserList, UserInstance, PostView

urlpatterns = patterns('workrave.cloud.views',
    url(r'^$', 'api_root'),
    url(r'^configuration/$', ConfigurationList.as_view(), name='configuration-list'),
    url(r'^configuration/(?P<pk>[0-9]+)/$', ConfigurationInstance.as_view(), name='configuration-detail'),
    url(r'^users/$', UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', UserInstance.as_view(), name='user-detail')
)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

urlpatterns += patterns('',
    url(r'^accounts/', include('allauth.urls')),

    url(r'^avatar/', include('avatar.urls')),
    url(r'^oauth2/', include('workrave.oauth2.urls', namespace = 'oauth2')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^stream1/$', RedisView.as_view(event_category="update"), name="stream1"),
    url(r'^post$', PostView.as_view()),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
