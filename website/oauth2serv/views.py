import logging
from urlparse import urlsplit
from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _

from .exceptions import OAuthError
from .settings import SESSION_AUTH_REQUEST_KEY
from .requests import AuthorizationRequest, AuthorizationCodeRequest, RefreshTokenRequest, TokenRequest

log = logging.getLogger(__name__)

class AuthorizationView(TemplateView):
    template_name = 'oauth2serv/authorize.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        response = super(AuthorizationView, self).dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'
        return response

    def exception_response(self, exception, auth_request):
        return self.error_response(exception.error, exception.detail, auth_request)

    def error_response(self, error, detail, auth_request):
        context = {
            'error': error,
            'error_description': u'%s' % detail
        }

        if auth_request is None:
            return self.render_to_response(context)
        else: 
            if auth_request.state is not None:
                context['state'] = auth_request.state
        
            if error in ['redirect_uri', 'unauthorized_client']:
                return self.render_to_response(context)
            else:
                uri = '%s?%s' % (auth_request.redirect_uri, '&'.join(['%s=%s' % (key, value) for key, value in context.items()]))
                return HttpResponseRedirect(uri)
        
    def get(self, request) : 
        try :
            auth_request = None
            if not request.is_secure() and not settings.DEBUG:
                raise OAuthError('invalid_request', _('A secure connection is required.'))
 
            request.session[SESSION_AUTH_REQUEST_KEY] = request.GET
        
            auth_request = AuthorizationRequest(request, request.GET)
            return auth_request.execute(self)
        
        except OAuthError, e:
            return self.exception_response(e, auth_request)

    def post(self, request) :
        try :
            auth_request = None
            if not request.is_secure() and not settings.DEBUG:
                raise OAuthError('invalid_request', _('A secure connection is required.'))
 
            original_request = request.session.get(SESSION_AUTH_REQUEST_KEY)
            auth_request = AuthorizationRequest(request, original_request, request.POST)
            response = auth_request.execute(self)
            del request.session[SESSION_AUTH_REQUEST_KEY]
            return response
            
        except OAuthError, e: 
            del request.session[SESSION_AUTH_REQUEST_KEY]
            return self.exception_response(e, auth_request)

        
class TokenView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        response = super(TokenView, self).dispatch(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'
        return response

    def exception_response(self, exception):
        return self.error_response(exception.error, exception.detail)

    def error_response(self, error, detail):
        context = {
            'error': error,
            'error_description': u'%s' % detail
        }

        return HttpResponse(simplejson.dumps(context), content_type='application/json;charset=UTF-8')        

    def post(self, request):
        try :
            if not request.is_secure() and not settings.DEBUG:
                raise OAuthError('invalid_request', _('A secure connection is required'))
 
            token_request = TokenRequest.create(request)
            return token_request.execute()
                
        except OAuthError, e: 
            return self.exception_response(e)
