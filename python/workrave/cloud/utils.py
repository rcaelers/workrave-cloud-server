from django.utils.importlib import import_module
import os
import gevent

from psycopg import make_psycopg_green

def make_django_green():
    from gevent import monkey
    monkey.patch_all()
    make_psycopg_green()
    
