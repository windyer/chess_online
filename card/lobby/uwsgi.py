"""
WSGI config for lobby project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""

import os
import sys

from django.core.handlers.wsgi import WSGIHandler
import go.logging

file_path = os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.pardir))
work_path = os.path.join(file_path, os.path.pardir)
sys.path.insert(0, work_path)
os.chdir(work_path)

go.logging.configure_root_logger('lobby')
application = WSGIHandler()