import logging
import json

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

        response = StreamingHttpResponse(self.iterator(), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response

    def iterator(self):
        connection = Redis(connection_pool=pool)
        pubsub = connection.pubsub()
        channel = self.event_category + '-' + self.request.user.username;
        pubsub.subscribe(channel)
        for message in pubsub.listen():
            if message['type'] == 'message':
                yield message['data']

def send_event(channel, json_data):
    connection = Redis(connection_pool=pool)
    connection.publish(channel, json_data)

__all__ = ['send_event', 'RedisView']
