import json

from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from workrave.cloud.redisview import send_event
from workrave.cloud.serializers import UserSerializer, ConfigurationSerializer, StateSerializer, StatisticsSerializer
from workrave.cloud.models import Configuration, State, Statistics, BreakStatistics
from workrave.cloud.permissions import IsOwner
from workrave.cloud.authentication import BearerTokenAuthentication

import django_filters

@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'users': reverse('cloud:user-list', request=request),
        'configuration': reverse('cloud:configuration-list', request=request),
        'statistics': reverse('cloud:statistics-list', request=request),
    })

class ConfigurationList(generics.ListCreateAPIView):
    model = Configuration
    serializer_class = ConfigurationSerializer
    permission_classes = ( IsOwner,)
    authentication_classes = ( BearerTokenAuthentication, SessionAuthentication, )

    def get_queryset(self):
        user = self.request.user
        return Configuration.objects.filter(owner=user)
    
    def pre_save(self, obj):
        obj.owner = self.request.user

        
class ConfigurationInstance(generics.RetrieveUpdateDestroyAPIView):
    model = Configuration
    serializer_class = ConfigurationSerializer
    authentication_classes = ( BearerTokenAuthentication, SessionAuthentication, )
    permission_classes = ( IsOwner, )

    def pre_save(self, obj):
        obj.owner = self.request.user

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        if pk == "me":
            return Configuration.objects.get(owner=self.request.user)
        else:
            obj = super(generics.RetrieveUpdateDestroyAPIView, self).get_object(queryset)
            if not self.has_permission(self.request, obj):
                self.permission_denied(self.request)
            return obj

class StateInstance(generics.RetrieveUpdateDestroyAPIView):
    model = State
    serializer_class = StateSerializer
    authentication_classes = ( BearerTokenAuthentication, SessionAuthentication, )
    permission_classes = ( IsOwner, )

    def pre_save(self, obj):
        obj.owner = self.request.user

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        if pk == "me":
            return State.objects.get(owner=self.request.user)
        else:
            obj = super(generics.RetrieveUpdateDestroyAPIView, self).get_object(queryset)
            if not self.has_permission(self.request, obj):
                self.permission_denied(self.request)
            return obj

class StatisticsFilter(django_filters.FilterSet):
    start = django_filters.DateFilter(name='date',lookup_type='gte')
    end = django_filters.DateFilter(name='date',lookup_type='lte')

    class Meta:
        model = Statistics
                    
class StatisticsList(generics.ListAPIView):
    model = Statistics
    serializer_class = StatisticsSerializer
    permission_classes = ( IsOwner,)
    filter_class = StatisticsFilter
    authentication_classes = ( BearerTokenAuthentication, SessionAuthentication, )

    def get_queryset(self):
        queryset = Statistics.objects.all()
        username = self.kwargs.get('username', None)
        if username is not None:
            if username == "me":
                username = self.request.user.username
            
            queryset = queryset.filter(owner__username=username)

        return queryset
        
    def pre_save(self, obj):
        obj.owner = self.request.user
        
class UserList(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer

class UserInstance(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer

class PostView(View):
    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        response = super(PostView, self).dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'
        return response

    def get(self, request) : 
        send_event('update-robc', json.dumps( {'hello': 'world', 'user': 'robc'}))
        send_event('update-orac', json.dumps( {'hello': 'world', 'user': 'orac'}))
        return HttpResponse()
        
    
