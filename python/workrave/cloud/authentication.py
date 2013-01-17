from rest_framework.authentication import BaseAuthentication

from workrave.oauth2.bearer import BearerAuth
from workrave.oauth2.exceptions import OAuthError


class BearerTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth=BearerAuth(request, ["https://api.workrave.org/workrave.state"])
        try:
            auth.validate()
        except OAuthError, e: 
            return None

        return (auth.user, None)
