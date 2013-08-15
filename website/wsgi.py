import os
import sys

from django.core.handlers.wsgi import WSGIHandler
sys.path = ['/home/ozancaglayan/webapps/newsdiffs/newsdiffs', '/home/ozancaglayan/webapps/newsdiffs/newsdiffs/website'] + sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'website.settings'
application = WSGIHandler()
