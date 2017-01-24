__all__ = ['RequestSerializationMiddleware']

from django.conf import settings
import go.logging
import go.containers

from card.core.util.mutex import Mutex

@go.logging.class_wrapper
class RequestSerializationMiddleware(object):

    def process_request(self, request):
        if hasattr(request, 'user'):
            user = request.user
            if hasattr(user, 'id') and user.id is not None:
                user_id = user.id
                timeout = settings.TIMEOUT.lock_timeout
                mutex = Mutex(user_id, timeout, go.containers.get_client())
                self.logger.debug('[request_lock_trace] [user|%s] locked in [mutex|%s]', user_id, mutex.key)                   
                mutex.lock()                                                  
                                                                               
    def process_response(self, request, response):
        if hasattr(request, 'user'):
            user = request.user
            if hasattr(user, 'id') and user.id is not None:
                user_id = user.id
                timeout = settings.TIMEOUT.lock_timeout
                mutex = Mutex(user_id, timeout, go.containers.get_client())
                self.logger.debug('[request_lock_trace] [user|%s] unlocked in [mutex|%s]', user_id, mutex.key)                   
                mutex.unlock()  

        return response 