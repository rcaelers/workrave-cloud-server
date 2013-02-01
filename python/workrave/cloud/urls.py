from django.conf.urls import patterns, include, url

from rest_framework.urlpatterns import format_suffix_patterns

from workrave.cloud.redisview import RedisView
from workrave.cloud.views import ConfigurationList, ConfigurationInstance, StateInstance, StatisticsList, StatisticsUpdate, UserList, UserInstance
from workrave.cloud.views import PostView, ActivateView, ClearView, RegisterView

urlpatterns = patterns('workrave.cloud.views',
    url(r'^$', 'api_root'),

    url(r'^configuration/$', ConfigurationList.as_view(), name='configuration-list'),
    url(r'^configuration/(?P<pk>\w+)/$', ConfigurationInstance.as_view(), name='configuration-detail'),

    url(r'^state/(?P<pk>\w+)/$', StateInstance.as_view(), name='state-detail'),

    url(r'^statistics/$', StatisticsList.as_view(), name='statistics-list'),
    url(r'^statistics/(?P<username>\w+)$', StatisticsList.as_view(), name='statistics-list'),
    url(r'^statistics/(?P<username>\w+)(?:/(?P<breakid>[a-zA-Z]+))?/(?P<setting>[a-zA-Z]+)/$', StatisticsUpdate.as_view(), name='statistics-update'),
    
    url(r'^users/$', UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', UserInstance.as_view(), name='user-detail')
)

# Format suffixes
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

urlpatterns += patterns('',
    url(r'^stream1/(?P<uuid>[0-9a-zA-Z]+)/$', RedisView.as_view(event_category="update"), name="stream1"),
    url(r'^activate/(?P<uuid>[0-9a-zA-Z]+)/(?P<txt>[0-9a-zA-Z]+)/$', ActivateView.as_view()),
    url(r'^clear/(?P<uuid>[0-9a-zA-Z]+)/(?P<txt>[0-9a-zA-Z]+)/$', ClearView.as_view()),
    url(r'^register/(?P<uuid>[0-9a-zA-Z]+)/$', RegisterView.as_view()),
)
    
