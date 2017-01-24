from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse

import go.logging
from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available

from card.lobby import permissions
import serializers
from .service import TurnerService

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'begin':reverse('begin', request=request, format=format),
        'gaming':reverse('gaming', request=request, format=format),
        'end':reverse('end', request=request, format=format)})

@go.logging.class_wrapper
class TurnerBegin(generics.CreateAPIView):

    serializer_class = serializers.TurnerBegin
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        service = TurnerService(request.service_repositories, 
                    request.activity_repository, request.counter_repository)
        game_status = service.turner_begin(request.user.id)
        serializer = self.get_serializer(game_status)
        return Response(serializer.data, status=status.HTTP_200_OK)

@go.logging.class_wrapper
class TurnerGaming(generics.CreateAPIView):
    serializer_class = serializers.TurnerGamingRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        turner_service = TurnerService(request.service_repositories, 
                        request.activity_repository, request.counter_repository)
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            game_status = turner_service.turner_gaming(request.user.id, **serializer.data)
            response_serializer = serializers.TurnerGamingReponse(game_status)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class TurnerEnd(generics.CreateAPIView):

    serializer_class = serializers.TurnerEndRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        service = TurnerService(request.service_repositories, 
                    request.activity_repository, request.counter_repository)
        game_status = service.turner_end(request.user.id)
        response_serializer = serializers.TurnerEndReponse(game_status)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
