import json

from datetime import datetime
from django.utils.timezone import utc

from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View

from rest_framework import generics, views
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework import status

from workrave.cloud.redisview import RedisView
from workrave.cloud.serializers import UserSerializer, ConfigurationSerializer, StateSerializer, StatisticsSerializer
from workrave.cloud.models import Configuration, State, Statistics, BreakStatistics, Client
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

class StatisticsUpdate(views.APIView):
    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username', None)
        if username == "me":
            username =  self.request.user.username

        try:
            stats = Statistics.objects.get(owner__username=username, date=datetime.now())
        except Statistics.DoesNotExist:
            micro_break = BreakStatistics()
            micro_break.save()
            rest_break = BreakStatistics()
            rest_break.save()
            daily_limit = BreakStatistics()
            daily_limit.save()
            stats = Statistics(owner=self.request.user, 
                               date = datetime.now(),
                               start_time = datetime.now(),
                               stop_time = datetime.now(),
                               micro_break = micro_break,
                               rest_break = rest_break,
                               daily_limit = daily_limit
                               )

        setting = self.kwargs.get('setting', None)
        breakid = self.kwargs.get('breakid', None)
        if breakid is not None:
            if breakid == 'm':
                b = stats.micro_break
            elif breakid == 'r':
                b = stats.rest_break
            elif breakid == 'd':
                b = stats.daily_limit

            # if not b return error
            setattr(b, setting, getattr(b, setting, 0) + 1)
            b.save()
            
        stats.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
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
        send_event('update-orac', json.dumps( {'hello': 'world', 'user': 'orac'}))
        return HttpResponse()
        
    
class ActivateView(View):
    def dispatch(self, request, *args, **kwargs):
        response = super(ActivateView, self).dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'
        return response

    def get(self, request, *args, **kwargs) : 
        uuid = kwargs.get('uuid', None)
        txt = kwargs.get('txt', "x")
        if uuid is not None:
            RedisView.send('workrave', 'activate', json.dumps( {'hello': 'world', 'user': 'robc', 'txt': txt}), request.user.username)
        return HttpResponse()
        
class ClearView(View):
    def dispatch(self, request, *args, **kwargs):
        response = super(ClearView, self).dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'
        return response

    def get(self, request, *args, **kwargs) : 
        uuid = kwargs.get('uuid', None)
        txt = kwargs.get('txt', "x")
        if uuid is not None:
            RedisView.send('update', 'clear', json.dumps( {'hello': 'world', 'user': 'robc', 'txt': txt}), request.user.username, uuid)
        return HttpResponse()

class RegisterView(View):
    def dispatch(self, request, *args, **kwargs):
        response = super(RegisterView, self).dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'
        return response

    def get(self, request, *args, **kwargs) : 
        uuid = kwargs.get('uuid', None)

        #client = Client(owner = requesr.user,
        #                last_seen = date=datetime.utcnow()
        #                uuid = uuid)
        
    
