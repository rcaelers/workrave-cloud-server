from django.conf.urls import patterns, include, url

from rest_framework.urlpatterns import format_suffix_patterns

from workrave.cloud.redisview import RedisView
from workrave.cloud.views import ConfigurationView, StateInstance, StatisticsView, StatisticsUpdateView, UserList, UserInstance
from workrave.cloud.views import PostView, ActivateView, ClearView, RegisterView, SignonView

urlpatterns = patterns('workrave.cloud.views',
    url(r'^$', 'api_root'),

    url(r'^configuration/((?P<username>\w+)/)?$', ConfigurationView.as_view(), name='configuration-detail'),

    url(r'^statistics/((?P<username>\w+)/)?$', StatisticsView.as_view(), name='statistics-detail'),
    url(r'^statistics/delta/(?P<username>\w+)/$', StatisticsUpdateView.as_view(delta=True), name='statistics-delta'),
    url(r'^statistics/set/(?P<username>\w+)/$', StatisticsUpdateView.as_view(delta=False), name='statistics-set'),
    
    url(r'^users/$', UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', UserInstance.as_view(), name='user-detail'),
)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

urlpatterns += patterns('',
    url(r'^signon/(?P<uuid>[-\w]+)/$', SignonView.as_view()),
    url(r'^stream1/(?P<uuid>[-\w]+)/$', RedisView.as_view(domain="workrave"), name='stream1'),
)
    
