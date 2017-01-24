__all__ = ['PreSessionMiddleware']

from django.conf import settings

class PreSessionMiddleware(object):

    def process_request(self, request):
        if settings.SESSION_COOKIE_NAME in request.GET:
            request.COOKIES[settings.SESSION_COOKIE_NAME] = \
                request.GET[settings.SESSION_COOKIE_NAME]