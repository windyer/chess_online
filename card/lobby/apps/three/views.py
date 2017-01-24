from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

import go.logging
from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available

from card.lobby import permissions
from card.lobby.apps.three import serializers
from card.lobby.apps.three.service import ThreeService

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({})

@go.logging.class_wrapper
class SelectGame(generics.CreateAPIView):

    serializer_class = serializers.ThreeServer
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None, **kwargs):
        request_serializer = serializers.SelectThreeRequest(data=kwargs)
        if request_serializer.is_valid():
            service = ThreeService(request.service_repositories, request.activity_repository)
            three_token = service.select_game(request.user.id, **request_serializer.data)
            serializer = self.get_serializer(three_token)
            return Response(serializer.data)
        else:
            from rest_framework import status
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)