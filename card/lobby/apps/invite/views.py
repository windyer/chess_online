from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
import go.logging
from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available
from card.lobby.apps.invite import serializers
from card.lobby.apps.invite.service import InviteService
import time
@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'invite_info':  reverse('invite-info', request=request, format=format),
        'award_info': reverse('award-info', request=request, format=format),
        'set_inviter': reverse('set-inviter', request=request, format=format),
        'get_award': reverse('get-award', request=request, format=format),
        })

@go.logging.class_wrapper
class InviteInfo(generics.CreateAPIView):
    serializer_class = serializers.InfoRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = InviteService(self.request.service_repositories, self.request.activity_repository)
            response = service.invite_info(**serializer.data)
            return Response(response)
        else:
            return Response(serializer.errors)


@go.logging.class_wrapper
class AwardInfo(generics.CreateAPIView):
    serializer_class = serializers.InfoRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = InviteService(self.request.service_repositories, self.request.activity_repository)
            response = service.award_info(**serializer.data)
            return Response(response)
        else:
            return Response(serializer.errors)

@go.logging.class_wrapper
class SetInviter(generics.CreateAPIView):
    serializer_class = serializers.SedInviterRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = InviteService(self.request.service_repositories, self.request.activity_repository)
            response = service.set_inviter(**serializer.data)
            return Response(response)
        else:
            return Response(serializer.errors)

@go.logging.class_wrapper
class GetAward(generics.CreateAPIView):
    serializer_class = serializers.InfoRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = InviteService(self.request.service_repositories, self.request.activity_repository)
            response = service.get_award(**serializer.data)
            return Response(response)
        else:
            return Response(serializer.errors)

