import functools
from rest_framework.response import Response
from django.http import HttpResponseServerError
from django.conf import settings

def api_view_available(available=settings.HOLYTREE.api_view_available):
    def _api_available(func):
        @functools.wraps(func)
        def _(request, format=None):
            if available:
                return func(request, format)
            else:
                return HttpResponseServerError("resourse can not find", 
                                                status=403, content_type="text/plain")
        return _
    return _api_available