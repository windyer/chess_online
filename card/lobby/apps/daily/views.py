from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

import go.logging

from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available
from card.lobby import permissions
from card.lobby.apps.daily.service import DailyService
from card.lobby.apps.daily import serializers

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'award':  reverse('award', request=request, format=format),
        'online-award':  reverse('online-award', request=request, format=format),
        })

@go.logging.class_wrapper
class Daily(generics.CreateAPIView):

    serializer_class = serializers.DailyRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        service = DailyService(request.service_repositories, request.activity_repository)
        response = service.get_daily_award(request.user.id)
        response_serializer = serializers.DailyResponse(response)
        return Response(response_serializer.data)

@go.logging.class_wrapper
class OnlineAward(generics.CreateAPIView):

    serializer_class = serializers.OnlineAwardRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        service = DailyService(request.service_repositories, request.activity_repository)
        response = service.get_online_award(request.user.id)
        response_serializer = serializers.OnlineAwardResponse(response)
        return Response(response_serializer.data)