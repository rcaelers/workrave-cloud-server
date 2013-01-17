from datetime import datetime
from django.utils.timezone import utc
import json

from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.timezone import utc

from .models import Token
from .exceptions import OAuthError

class BearerAuth():
    request = None
    scopes = None
    user = None
        
    def __init__(self, request, scopes):
        self.request = request
        self.scopes = scopes

    def response(self, exception):
        return self.error_response(exception.error, exception.detail)
        
    def error_response(self, error, detail) :
        error_status =  {
            'invalid_request'    : 400,
            'invalid_token'      : 401,
            'insufficient_scope' : 403
            }
       
        status = error_status[error]

        context = {
            'error': error,
            'error_description': u'%s' % detail
            }

        return HttpResponse(json.dumps(context), 
                            content_type='application/json;charset=UTF-8',
                            status=status
                            )

    def validate(self):
        access_token = None
        
        auth = self.request.META.get('HTTP_AUTHORIZATION')
        if auth is not None:
            method, value = auth.split(' ')
            if method == 'Bearer':
                access_token = value

        if access_token is None:
            access_token = self.request.REQUEST.get('access_token')

        if access_token is None:
            raise OAuthError('invalid_token', 'Request does not contain a valid access token')

        try:
            token = Token.objects.get(access_token=access_token, expires__gt=datetime.utcnow())
        except ObjectDoesNotExist:
            raise OAuthError('invalid_token', 'Request contains a invalid access token')

        if self.scopes is not None:
            if token.scopes.filter(name__in=self.scopes).count() != len(self.scopes):
                raise OAuthError('insufficient_scope', '')

        self.user = token.user
        
    def login(self):
        if not hasattr(self.user, 'backend'):
            self.user.backend = "django.contrib.auth.backends.ModelBackend"
            login(self.request, self.user)
