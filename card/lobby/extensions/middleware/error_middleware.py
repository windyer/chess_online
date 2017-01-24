__all__ = ['ErrorMiddleware']

import traceback
import json

from _mysql_exceptions import OperationalError
import redis

from django.conf import settings
from django.http import HttpResponseServerError
from go.error import Warning, Error
from go.protobuf import NetworkError

from card.core.error.common import CoreError

class ErrorMiddleware(object):

    def _exception_convert(self, request, exception):
        if isinstance(exception, NetworkError.CONNECTION_LOST):
            raise CoreError.DB_CONNECTION_LOST()
        elif isinstance(exception, redis.exceptions.ConnectionError):
            raise CoreError.REDIS_CONNECTION_FAILED()
        elif isinstance(exception, OperationalError):
            raise CoreError.MYSQL_CONNECTION_FAILED()
        else:
            raise

    def process_exception(self, request, exception):
        try:
            self._exception_convert(request, exception)
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
                return HttpResponseServerError("server interner error", 
                                            content_type="text/plain")
