from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import go.logging

from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available
from card.lobby.apps.update.service import UpdateService
from card.lobby.apps.update import serializers

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        })

@go.logging.class_wrapper
class LatestVersion(generics.RetrieveAPIView):

    serializer_class = serializers.UpdateRequest
    permission_classes = ()

    @trace_view
    def get(self, request, format=None, **kwargs):
        serializer = self.get_serializer(data=kwargs)
        if serializer.is_valid():
            service = UpdateService()
            version_info = service.get_latest_version(**serializer.data)
            version_info['disable_encoder'] = False
            return Response(version_info)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)