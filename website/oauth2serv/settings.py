import logging
from django.conf import settings as _settings

LOGGER = logging.getLogger('django.oauth2serv')

SCOPE_LENGTH = getattr(_settings, 'OAUTH2SERV_SCOPE_LENGTH', 255)

CLIENT_ID_LENGTH = getattr(_settings, 'OAUTH2SERV_CLIENT_ID_LENGTH', 32)

CLIENT_SECRET_LENGTH = getattr(_settings, 'OAUTH2SERV_CLIENT_SECRET_LENGTH', 32)

CODE_LENGTH = getattr(_settings, 'OAUTH2SERV_CODE_LENGTH', 32)

CODE_LIFETIME = getattr(_settings, 'OAUTH2SERV_CODE_LIFETIME', 120)

ACCESS_TOKEN_LENGTH = getattr(_settings, 'OAUTH2SERV_ACCESS_TOKEN_LENGTH', 32)

REFRESH_TOKEN_LENGTH = getattr(_settings, 'OAUTH2SERV_REFRESH_TOKEN_LENGTH', 32)

ACCESS_TOKEN_LIFETIME = getattr(_settings, 'OAUTH2SERV_ACCESS_TOKEN_LIFETIME', 3600)

SESSION_AUTH_REQUEST_KEY = 'oauth2serv:request'
