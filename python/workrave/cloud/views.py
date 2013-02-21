import json

from datetime import datetime
from django.utils.timezone import utc

from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.utils.dateparse import parse_date, parse_datetime
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, views
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse 
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
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
    return Response(
        {
            'users': reverse('cloud:user-list', request=request),
            'configuration': reverse('cloud:configuration-detail', request=request),
            'statistics': reverse('cloud:statistics-detail', request=request),
            'state': reverse('cloud:state-detail', request=request)
        }
    )


class ConfigurationView(generics.RetrieveUpdateAPIView):
    model = Configuration
    serializer_class = ConfigurationSerializer
    authentication_classes = ( BearerTokenAuthentication, SessionAuthentication, )
    permission_classes = ( IsOwner, )

    def pre_save(self, obj):
        obj.owner = self.request.user

    def get_object(self, queryset=None):
        username = self.kwargs.get('username', None)
        if username == "me" or username is None:
            username =  self.request.user.username

        obj = Configuration.objects.get(owner__username=username)
            
        if not self.has_permission(self.request, obj):
            self.permission_denied(self.request)

        return obj

class StatisticsFilter(django_filters.FilterSet):
    start = django_filters.DateFilter(name='date',lookup_type='gte')
    end = django_filters.DateFilter(name='date',lookup_type='lte')

    class Meta:
        model = Statistics
                    
class StatisticsView(generics.ListAPIView):
    model = Statistics
    serializer_class = StatisticsSerializer
    authentication_classes = ( BearerTokenAuthentication, SessionAuthentication)
    permission_classes = ( IsAuthenticated, IsOwner, )
    filter_class = StatisticsFilter
    paginate_by = 10
    paginate_by_param = 'page_size'
    
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


class StatisticsUpdateView(generics.GenericAPIView):
    delta = True
    model = Statistics
    serializer_class = StatisticsSerializer
    authentication_classes = ( BearerTokenAuthentication, SessionAuthentication)
    permission_classes = ( IsAuthenticated, )

    def pre_save(self, obj):
        obj.owner = self.request.user

    def post(self, request, *args, **kwargs):
        username = self.kwargs.get('username', None)
        if username == "me":
            username =  self.request.user.username

        data = request.DATA
        
        if not 'date' in data:
            raise ParseError('date missing')

        day = parse_date(data['date'])
        if day is None:
            raise ParseError('date malformed')

        try:
            
            stats = Statistics.objects.get(owner__username=username, 
                                           date=datetime.strptime(request.DATA['date'], '%Y-%m-%d'))
        except:
            micro_break = BreakStatistics()
            micro_break.save()
            rest_break = BreakStatistics()
            rest_break.save()
            daily_limit = BreakStatistics()
            daily_limit.save()
            stats = Statistics(owner=self.request.user, 
                               date = datetime.now(),
                               start_time = datetime.utcnow().replace(tzinfo=utc),
                               stop_time = datetime.utcnow().replace(tzinfo=utc),
                               micro_break = micro_break,
                               rest_break = rest_break,
                               daily_limit = daily_limit
                               )
        
        breaks = [ 'micro_break', 'rest_break', 'daily_limit' ]
        break_attr = ['prompted', 'taken', 'natural_taken', 'skipped', 'postponed', 'unique', 'total_overdue' ]
        general_attr = [ 'total_active_time', 'total_click_movement', 'total_mouse_movement' ,
                         'total_movement_time', 'total_clicks', 'total_keystrokes']

        if 'start_time' in data:
            start_time = parse_datetime(data['start_time'])
            if start_time is None:
                raise ParseError('start time malformed')

            if start_time < stats.start_time:
                stats.start_time = start_time;
        
        if 'stop_time' in data:
            stop_time = parse_datetime(data['stop_time'])
            if stop_time is None:
                raise ParseError('stop time malformed')

            if stop_time > stats.stop_time:
                stats.stop_time = stop_time;
        
        for attr in general_attr:
            if attr in data:
                setattr(stats, attr, getattr(stats, attr, 0) + data[attr])
        
        for id in breaks:
            if not id in data:
                continue
            
            break_data = data[id]
            break_model = getattr(stats, id, None)
        
            if break_model is None:
                continue

            modified = False
            for attr in break_attr:
                if attr in break_data:
                    setattr(break_model, attr, getattr(break_model, attr, 0) + break_data[attr])
                    modified = True
            if modified:
                break_model.save()

        stats.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
            
class StateInstance(generics.RetrieveUpdateAPIView):
    model = State
    serializer_class = StateSerializer
    authentication_classes = ( BearerTokenAuthentication, SessionAuthentication, )
    permission_classes = ( IsOwner, )

    def pre_save(self, obj):
        obj.owner = self.request.user

    def get_object(self, queryset=None):
        username = self.kwargs.get('username', None)
        if username == "me" or username is None:
            return State.objects.get(owner=self.request.user)
        else:
            obj = super(generics.RetrieveUpdateDestroyAPIView, self).get_object(queryset)
            if not self.has_permission(self.request, obj):
                self.permission_denied(self.request)
            return obj
            
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
        
   
class SignonView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        response = super(SignonView, self).dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'
        return response

    def post(self, request, *args, **kwargs) : 
        uuid = kwargs.get('uuid', None)
        print uuid

        data = json.loads(request.body)
        print data
        print uuid

        print 
        
        reply ={ 'event_url' : reverse('cloud:stream1', kwargs={'uuid': uuid}, request=request) }
                            
        return HttpResponse(json.dumps(reply), content_type='application/json;charset=UTF-8')        
