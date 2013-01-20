from workrave.cloud.utils import make_django_green
make_django_green()

from gevent.pywsgi import WSGIServer
import gevent
import sys

from django.core.management.commands.runserver import BaseRunserverCommand

class Command(BaseRunserverCommand):
    help = "Runs the gevent web server."

    def inner_run(self, *args, **options):
        self.validate(display_num_errors=True)
        try:
            handler = self.get_handler(*args, **options)
            run(self.addr, int(self.port), handler)
        except KeyboardInterrupt:
            sys.exit(0)
    
def run(addr, port, wsgi_handler):
    server_address = (addr, port)
    httpd = WSGIServer(server_address, wsgi_handler)
    httpd.serve_forever()

