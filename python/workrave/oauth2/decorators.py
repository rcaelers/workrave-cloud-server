from functools import wraps
from django.utils.decorators import available_attrs

from .bearer import BearerAuth
from .exceptions import OAuthError

def require_oauth_scope(scope_list):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def inner(request, *args, **kwargs):
            auth=BearerAuth(request, scope_list)
            try:
                auth.validate()
                auth.login()
            except OAuthError, e: 
                return auth.response(e)

            return func(request, *args, **kwargs)
        return inner
    return decorator
