__all__ = ['PostSessionMiddleware']

from django.conf import settings
from django.http import HttpResponseRedirect

class PostSessionMiddleware(object):

    def process_request(self, request):
        if settings.SESSION_COOKIE_NAME in request.GET:
            #request.session.accessed = True
            request.session.modified = True
            return HttpResponseRedirect(request.path)
