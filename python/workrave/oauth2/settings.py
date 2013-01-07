import logging
from django.conf import settings as _settings

LOGGER = logging.getLogger('django.oauth2')

SCOPE_LENGTH = getattr(_settings, 'OAUTH2_SCOPE_LENGTH', 255)

CLIENT_ID_LENGTH = getattr(_settings, 'OAUTH2_CLIENT_ID_LENGTH', 32)

CLIENT_SECRET_LENGTH = getattr(_settings, 'OAUTH2_CLIENT_SECRET_LENGTH', 32)

CODE_LENGTH = getattr(_settings, 'OAUTH2_CODE_LENGTH', 32)

CODE_LIFETIME = getattr(_settings, 'OAUTH2_CODE_LIFETIME', 120)

ACCESS_TOKEN_LENGTH = getattr(_settings, 'OAUTH2_ACCESS_TOKEN_LENGTH', 32)

REFRESH_TOKEN_LENGTH = getattr(_settings, 'OAUTH2_REFRESH_TOKEN_LENGTH', 32)

ACCESS_TOKEN_LIFETIME = getattr(_settings, 'OAUTH2_ACCESS_TOKEN_LIFETIME', 3600)

SESSION_AUTH_REQUEST_KEY = 'oauth2:request'
