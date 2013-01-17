from django.conf.urls import patterns, include, url

from rest_framework.urlpatterns import format_suffix_patterns

from workrave.cloud.redisview import RedisView
from workrave.cloud.views import ConfigurationList, ConfigurationInstance, StateInstance, StatisticsList, UserList, UserInstance, PostView

urlpatterns = patterns('workrave.cloud.views',
    url(r'^$', 'api_root'),

    url(r'^configuration/$', ConfigurationList.as_view(), name='configuration-list'),
    url(r'^configuration/(?P<pk>\w+)/$', ConfigurationInstance.as_view(), name='configuration-detail'),

    url(r'^state/(?P<pk>\w+)/$', StateInstance.as_view(), name='state-detail'),

    url(r'^statistics/$', StatisticsList.as_view(), name='statistics-list'),
    url(r'^statistics/(?P<username>\w+)$', StatisticsList.as_view(), name='statistics-list'),
    
    url(r'^users/$', UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', UserInstance.as_view(), name='user-detail')
)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

urlpatterns += patterns('',
    url(r'^stream1/$', RedisView.as_view(event_category="update"), name="stream1"),
    url(r'^post$', PostView.as_view()),
    )
    
