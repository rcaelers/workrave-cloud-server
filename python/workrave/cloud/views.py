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

from workrave.cloud.redisview import send_event
from workrave.cloud.serializers import UserSerializer, ConfigurationSerializer
from workrave.cloud.models import Configuration
from workrave.cloud.permissions import IsOwner

@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'users': reverse('user-list', request=request),
        'configuration': reverse('configuration-list', request=request),
    })

class ConfigurationList(generics.ListCreateAPIView):
    model = Configuration
    serializer_class = ConfigurationSerializer
    permission_classes = ( IsOwner,)

    def pre_save(self, obj):
        obj.owner = self.request.user

        
class ConfigurationInstance(generics.RetrieveUpdateDestroyAPIView):
    model = Configuration
    serializer_class = ConfigurationSerializer
    #permission_classes = ( IsOwner,)

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
        
    
