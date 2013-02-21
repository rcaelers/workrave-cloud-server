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
    domain = 'general'

    @method_decorator(csrf_exempt)
    @method_decorator(require_oauth_scope(["https://api.workrave.org/workrave.state"]))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.uuid = self.kwargs.get('uuid', None)

        self.username = request.user.username
        
        response = StreamingHttpResponse(self.iterator(), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response

    @classmethod
    def send(cls, domain, event_name, event_data, username, destination = "+"):
        feed_name = username + ":" + destination + ":" + domain
        feed_key = 'data/' + feed_name

        dump = pickle.dumps((domain, event_name, event_data))
        connection = Redis(connection_pool=pool)

        previous_dump = connection.hget(feed_key, event_name)
        if dump == previous_dump:
            return
        
        connection.hset(feed_key, event_name, dump)
        connection.publish(feed_name, dump)

    def iterator(self):
        connection = Redis(connection_pool=pool)
        pubsub = connection.pubsub()
        
        channel = self.username + ':*:' + self.domain
        pubsub.psubscribe(channel)

        for key in connection.keys('data/' + channel):
            for event_key in connection.hkeys(key):
                event_dump = connection.hget(key, event_key)
                yield pickle.loads(event_dump)

        for message in pubsub.listen():
            if message['type'] == 'pmessage':
                event_dump = message['data']
                yield pickle.loads(event_dump)
                    
__all__ = ['RedisView']
