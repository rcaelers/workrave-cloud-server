import time
from datetime import timedelta
from hashlib import sha512
from uuid import uuid4

from django.utils import timezone

def generate_key(length) :
    return sha512(uuid4().hex).hexdigest()[0:length]

def generate_timestamp(delta) :
    return timezone.now() + timedelta(seconds=delta)

