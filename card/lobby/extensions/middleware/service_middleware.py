__all__ = ['ServiceMiddleware']

import json

from django.http import HttpResponseServerError
from django.conf import settings

from go.error import Warning, Error
from card.api.service_repository import ServiceRepository


class ServiceMiddleware(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if not request.path.startswith(settings.STATIC_URL):
                request.service_repositories = ServiceRepository(settings.SERVICE_REPOSITORYS)
        except (Warning, Error) as ex:
            data = {}
            data['code'] = ex.CODE
            if settings.DEBUG:
                data['message'] = ex.message
            data = json.dumps(data)
            return HttpResponseServerError(data, status=501, content_type='application/json')
        except Exception:
            if settings.DEBUG:
                raise
            else:
                HttpResponseServerError("server interner error", 
                                    content_type="text/plain")

    def process_response(self, request, response):
        if hasattr(request, 'service_repositories'):
            request.service_repositories.close()
            request.service_repositories = None
            del request.service_repositories
        return response

    def process_exception(self, request, exception):
        if hasattr(request, 'service_repositories'):
            request.service_repositories.close()
            request.service_repositories = None
            del request.service_repositories
