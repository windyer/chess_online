__all__ = ['ActivityMiddleware']

from django.http import HttpResponseServerError
from django.conf import settings

from go.error import Warning, Error
from card.lobby.apps.activity.base import ActivityRepository


class ActivityMiddleware(object):

    activity_repository = None

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.path.startswith(settings.STATIC_URL):
            if ActivityMiddleware.activity_repository is None:
                ActivityMiddleware.activity_repository = ActivityRepository()
            request.activity_repository = ActivityMiddleware.activity_repository