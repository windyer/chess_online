__all__ = ['DurableCounterMiddleware']

from django.http import HttpResponseServerError
from django.conf import settings

from go.error import Warning, Error
from card.core.statistics.durable_counter import CounterRepository


class DurableCounterMiddleware(object):

    counter_repository = None

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.path.startswith(settings.STATIC_URL):
            if DurableCounterMiddleware.counter_repository is None:
                DurableCounterMiddleware.counter_repository = CounterRepository()
                DurableCounterMiddleware.counter_repository.load()
            request.counter_repository = DurableCounterMiddleware.counter_repository