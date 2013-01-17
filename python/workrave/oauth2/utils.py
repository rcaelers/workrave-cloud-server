from datetime import datetime
from datetime import timedelta
from hashlib import sha512
from uuid import uuid4

from django.utils import timezone
from django.utils.timezone import utc

class TokenGenerator(object):
    def __init__(self, length):
        self.length = length

    def __call__(self):
        return sha512(uuid4().hex).hexdigest()[0:self.length]

class TimestampGenerator(object):
    def __init__(self, delta=0):
        self.delta = delta

    def __call__(self):
        return datetime.utcnow() + timedelta(seconds=self.delta)
