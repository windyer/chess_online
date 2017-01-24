from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

import go.logging
from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available

from card.lobby import permissions
import serializers
from .service import GameService

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'quick-game':  reverse('quick-game', request=request, format=format),
        })

@go.logging.class_wrapper
class QuickGame(generics.CreateAPIView):

    serializer_class = serializers.GameServer
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        service = GameService(request.service_repositories, 
                                request.activity_repository)
        try:
            game_token = service.quick_game(request.user.id)
        except Exception as ex:
            from rest_framework import status
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(game_token)
        return Response(serializer.data)


@go.logging.class_wrapper
class SelectGame(generics.CreateAPIView):

    serializer_class = serializers.GameServer
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None, **kwargs):
        request_serializer = serializers.SelectGameRequest(data=kwargs)
        if request_serializer.is_valid():
            service = GameService(request.service_repositories, 
                                request.activity_repository)
            try:
                game_token = service.select_game(request.user.id, **request_serializer.data)
            except Exception as ex:
                from rest_framework import status
                return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(game_token)
            return Response(serializer.data)
        else:
            from rest_framework import status
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class FollowGame(generics.CreateAPIView):

    serializer_class = serializers.GameServer
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None, **kwargs):
        request_serializer = serializers.FollowGameRequest(data=kwargs)

        if request_serializer.is_valid():
            service = GameService(request.service_repositories, 
                                request.activity_repository)
            try:
                game_token = service.follow_game(request.user.id, **request_serializer.data)
            except Exception as ex:
                from rest_framework import status
                return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(game_token)
            return Response(serializer.data)
        else:
            from rest_framework import status
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
