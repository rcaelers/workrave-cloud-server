from django.conf.urls.defaults import patterns

from . import views

urlpatterns = patterns('',
    (r'^authorize/$', views.AuthorizationView.as_view()),
    (r'^token/$', views.TokenView.as_view()),
)
