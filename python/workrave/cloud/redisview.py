import logging
import json

try:
   import cPickle as pickle
except:
   import pickle

from django.conf import settings
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import StreamingHttpResponse

from redis import ConnectionPool as ConnectionPool
from redis import Redis
from redis.connection import UnixDomainSocketConnection, Connection

from workrave.oauth2.decorators import require_oauth_scope

log = logging.getLogger(__name__)

REDIS_CONNECTION_SETTINGS = {
    'host': 'localhost',
    'port' : 6379,
    'db': 0,
}

pool = ConnectionPool(**REDIS_CONNECTION_SETTINGS)

class RedisView(View):
    event_category = 'event'

    @method_decorator(csrf_exempt)
    @method_decorator(require_oauth_scope(["https://api.workrave.org/workrave.state"]))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.uuid = self.kwargs.get('uuid', None)

        self.username = request.user.username
        self.data_key = 'events.data.' + self.username
        
        response = StreamingHttpResponse(self.iterator(), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response

    @classmethod
    def send(cls, event_category, event_name, event_data, username, uuid = None):
        full_name = event_category + ':' + event_name
        dump = pickle.dumps((full_name, event_data))
        connection = Redis(connection_pool=pool)
        connection.hset('events.data.' + username, full_name, dump)

        if uuid is not None:
            channel = username + ':' + uuid + ':' + event_category
            connection.publish(channel, dump)

        channel = username + ':all:' + event_category
        connection.publish(channel, dump)
            
    def iterator(self):
        connection = Redis(connection_pool=pool)
        pubsub = connection.pubsub()
        
        channel = self.username + ':all:' + self.event_category
        pubsub.subscribe(channel)
        channel = self.username + ':' + self.uuid + ':' + self.event_category
        pubsub.subscribe(channel)
        
        if connection.exists(self.data_key):
            for name in connection.hkeys(self.data_key):
                event_dump = connection.hget(self.data_key, name)
                print 'NAME', name
                
                (event_full_name, event_data) = event = pickle.loads(event_dump)
                yield event

        for message in pubsub.listen():
            if message['type'] == 'message':
                event_dump = message['data']
                event = pickle.loads(event_dump)
                yield event

                    
__all__ = ['RedisView']
