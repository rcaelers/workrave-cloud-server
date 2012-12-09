import logging
from urlparse import urlsplit
from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.utils import simplejson
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _

from .models import Client, Scope, CodeGrant, Token
from .forms import AuthorizationForm
from .exceptions import OAuthError
from .settings import SESSION_AUTH_REQUEST_KEY

log = logging.getLogger(__name__)

class AuthorizationRequest(object) :
    def __init__(self, request, data, post_data = None):
        self.user = request.user
        self.request = request
        self.data = data
        self.post_data = post_data
        
        self.client_id = data.get('client_id')
        self.redirect_uri = data.get('redirect_uri')
        self.response_type = data.get('response_type')
        self.scope = data.get('scope')
        self.state = data.get('state')
        self.info = data.get('krandor_extra_info', '')
        self.tagline = ''

        self.validate(request)

    def validate(self, request) : 
        if self.user != request.user:
            raise OAuthError('invalid_request', _('The authenticated user changed during authorization'))

        self.validate_client()
        self.validate_redirect_uri()
        self.validate_scope()
        
        if self.response_type not in [ 'code' ]:
            raise OAuthError('unsupported_response_type', _('Reponse type not supported: %s') % self.response_type)
            
    def validate_client(self) : 
        if self.client_id is None:
            raise OAuthError('invalid_request', _('Missing required parameter: client_id'))

        try:
            self.client = Client.objects.get(client_id=self.client_id)
        except Client.DoesNotExist:
            raise OAuthError('unauthorized_client', _('The client is not authorized'))
        
    def validate_redirect_uri(self) : 
        if self.redirect_uri is None:
            self.redirect_uri = client.redirect_uri

        if self.client.profile == Client.PROFILE_NATIVE:
            uri = urlsplit(self.redirect_uri)
            if not uri.scheme in ['http', 'https']:
                raise OAuthError('redirect_uri', _('Illegal redirect. Native applications must redirect to http or https'))
            if not uri.hostname in [ 'localhost', '127.0.0.1' ]:
                raise OAuthError('redirect_uri', _('Illegal redirect. Native applications must redirect to localhost'))
            if uri.fragment != '':
                raise OAuthError('redirect_uri', _('Illegal redirect. Native applications may not specify a fragment in their redirect'))

        elif self.client.profile == Client.PROFILE_WEB:
            # TODO: should the redirect be normalized?
            if self.redirect_uri != client.redirect_uri:
                raise OAuthError('redirect_uri', _('Illegal redirect. Untrusted URI not allowed'))
            
        else:
            raise OAuthError('server_error', _('Configuration error. Unsupported client profile'))

    def get_allowed_scopes(self) : 
        allowed_scopes = []
        if self.client.scopes.all():
            for scope in self.client.scopes.all():
                allowed_scopes.append(scope)
        else:
            for scope in Scope.objects.all():
                allowed_scopes.append(scope)
        return allowed_scopes
        
    def validate_scope(self) : 
        if self.scope is not None:
            requested_scopes = self.scope.split(' ')
        else:
            requested_scopes = []

        allowed_scopes = self.get_allowed_scopes()
        self.scopes = [ scope for scope in allowed_scopes if scope.name in requested_scopes ]

    def limit_scopes(self, limited_scopes) : 
        allowed_scopes = self.get_allowed_scopes()
        self.scopes = [ scope for scope in self.scopes if (scope.name in limited_scopes and scope in allowed_scopes)] 

    def create_autorization_grant_code(self) :
        code_grant = CodeGrant(user=self.user, 
                               client=self.client, 
                               description=self.info,
                               tagline=self.tagline,
                               redirect_uri=self.redirect_uri)

        code_grant.save()

        for scope in self.scopes:
            code_grant.scopes.add(scope)
            
        return code_grant

    def execute(self, view):
        authorization_form = AuthorizationForm(self.post_data)

        if not (authorization_form.is_bound and authorization_form.is_valid()):
            return view.render_to_response({
                'client': self.client,
                'form': authorization_form,
                'scopes': self.scopes, })
        
        if self.request.POST.get('authorize') is None:
            raise OAuthError('access_denied', _('User refused authorization'))

        self.tagline = self.request.POST.get('tagline', '')
        self.limit_scopes(self.request.POST.getlist('scopes', []))
                
        code_grant = self.create_autorization_grant_code()
        
        query = QueryDict('', mutable=True)

        if self.state is not None:
            query['state'] = self.state
            
        query['code'] = code_grant.code
            
        redirect_uri = '%s?%s' % (self.redirect_uri, '&'.join(['%s=%s' % (key, value) for key, value in query.items()]))
        return HttpResponseRedirect(redirect_uri)

class TokenRequest(object) :
    def __init__(self, request):
        self.request = request

        self.client_id = None
        self.client_secret = None
        
        self.authenticate()

    def authenticate(self):
        auth = self.request.META.get('HTTP_AUTHORIZATION')

        if auth is not None:
            try:
                method, value = auth.split(' ')
                if method == 'Basic':
                    self.client_id, self.client_secret = value.decode('base64').split(':')
            except ValueError, e:
                pass

        if self.client_id is None:
            self.client_id = self.request.POST.get('client_id')
            self.client_secret = self.request.POST.get('client_secret')
            
        if self.client_id is None:
            raise OAuthError('invalid_request', _('Missing required parameter: client_id'))

        try:
            self.client = Client.objects.get(client_id=self.client_id)
        except Client.DoesNotExist:
            raise OAuthError('unauthorized_client', _('The client is not authorized'))

    @classmethod
    def create(cls, request, *args, **kwargs) : 
        grant_type = request.POST.get('grant_type')

        if self.grant_type is None:
            raise OAuthError('invalid_request', 'Missing required parameter: grant_type')
        
        if grant_type  == 'authorization_code': 
            obj = AuthorizationCodeRequest(request)
        elif grant_type == 'refresh_token':
            obj = RefreshTokenRequest(request)
        else:
            raise OAuthError('unsupported_grant_type', _('Grant type not supported: %s') % grant_type)

        return obj

class AuthorizationCodeRequest(TokenRequest) :
    def __init__(self, request):
        super(AuthorizationCodeRequest, self).__init__(request)
        self.validate()
    
    def validate(self) : 
        self.code = self.request.POST.get('code')
        self.redirect_uri = self.request.POST.get('redirect_uri')

        if self.code is None:
            raise OAuthError('invalid_request', _('Missing required parameter: code'))
            
        try:
            self.code_grant = CodeGrant.objects.get(code=self.code, client=self.client, expires__gt=datetime.now())
        except CodeGrant.DoesNotExist:
            raise OAuthError('invalid_grant', _('Invalid grant'))

        previous_tokens = Token.objects.filter(code=self.code).all()
        if len(previous_tokens) > 0:
            previous_tokens.delete()
            raise OAuthError('invalid_grant', _('Grant used more than once. Revoking'))

        if self.redirect_uri is None:
            raise OAuthError('invalid_request', _('Missing required parameter: redirect_uri'))

        if self.redirect_uri !=  self.code_grant.redirect_uri:
            raise OAuthError('invalid_request', _('redirect_uri mismatch'))

        if self.client != self.code_grant.client:
            raise OAuthError('invalid_request', _('client mismatch'))

    def execute(self):
        token = Token.objects.create( user=self.code_grant.user,
                                      client=self.client,
                                      code=self.code,
                                      description=self.code_grant.description,
                                      tagline=self.code_grant.tagline)
        token.save()

        for scope in self.code_grant.scopes.all():
            token.scopes.add(scope)

        self.code_grant.delete()

        now = datetime.utcnow().replace(tzinfo=utc)
        
        return HttpResponse(simplejson.dumps({'access_token': token.access_token,
                                              'expires_in': (token.expires - now).seconds,
                                              'refresh_token': token.refresh_token,
                                              'scope': ' '.join([scope.name for scope in token.scopes.all()]),
                                              }), content_type='application/json;charset=UTF-8')        
        
        
class RefreshTokenRequest(TokenRequest) :
    def __init__(self, request):
        super(RefreshTokenRequest, self).__init__(request)

    def validate(self):
        self.refresh_token = self.request.POST.get('refresh_token')

        if self.refresh_token is None:
            raise OAuthError('invalid_request', 'Missing required parameter: refresh_token')
            
        try:
            self.token = Token.objects.get(refresh_token=self.refresh_token, expires__gt=datetime.now())
        except CodeGrant.DoesNotExist:
            raise OAuthError('invalid_grant', _('Invalid grant'))

        if self.client != self.code_grant.client:
            raise OAuthError('invalid_request', 'client mismatch')

    def execute(self):
        now = datetime.utcnow().replace(tzinfo=utc)

        self.token.created_date = now
        self.token.access_token = generate_key(ACCESS_TOKEN_LENGTH)
        self.token.refresh_token = generate_key(REFRESH_TOKEN_LENGTH)
        self.token.token.save()

        return HttpResponse(simplejson.dumps({'access_token': token.access_token,
                                              'expires_in': (token.expires - now).seconds,
                                              'refresh_token': token.refresh_token,
                                              'scope': ' '.join([scope.name for scope in token.scopes.all()]),
                                              }), content_type='application/json;charset=UTF-8')        
