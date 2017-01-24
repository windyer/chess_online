from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status
import go.logging

from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available
from card.lobby import permissions
from card.lobby.apps.freebie.service import FreebieService
from card.lobby.apps.freebie import serializers

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'salvage':  reverse('salvage', request=request, format=format),
        'money_tree':  reverse('money-tree', request=request, format=format),
        'wall/ios/youmi':  reverse('youmi-ios-wall', request=request, format=format),
        'wall/android/youmi':  reverse('youmi-android-wall', request=request, format=format),
        'wall/ios/domob':  reverse('domob-ios-wall', request=request, format=format),
        'wall/ios/limei':  reverse('limei-ios-wall', request=request, format=format),
        })


@go.logging.class_wrapper
class Salvage(generics.CreateAPIView):

    serializer_class = serializers.SalvageResponse
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None, **kwargs):
        service = FreebieService(request.service_repositories, request.activity_repository)
        response = service.get_salvage_fund(request.user.id)
        serializer = self.get_serializer(response)
        return Response(serializer.data)

@go.logging.class_wrapper
class MoneyTree(generics.CreateAPIView):

    serializer_class = serializers.MoneyTreeResponse
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None, **kwargs):
        service = FreebieService(request.service_repositories, request.activity_repository)
        response = service.get_money_tree_award(request.user.id)
        serializer = self.get_serializer(response)
        return Response(serializer.data)

@go.logging.class_wrapper
class YoumiIosWall(generics.ListAPIView):

    serializer_class = serializers.IosYouMiRequest

    @trace_view
    def get(self, request, format=None, **kwargs):
        serializer = self.get_serializer(data=dict(request.QUERY_PARAMS.iteritems()))
        if serializer.is_valid():
            service = FreebieService(request.service_repositories, request.activity_repository)
            try:
                service.process_ios_youmi_wall_order(**serializer.data)
            except Exception as ex:
                self.logger.exception(ex)
                return Response({}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class YoumiAndroidWall(generics.ListAPIView):

    serializer_class = serializers.AndroidYouMiRequest

    @trace_view
    def get(self, request, format=None, **kwargs):
        serializer = self.get_serializer(data=dict(request.QUERY_PARAMS.iteritems()))
        if serializer.is_valid():
            service = FreebieService(request.service_repositories, request.activity_repository)
            try:
                service.process_android_youmi_wall_order(**serializer.data)
            except Exception as ex:
                self.logger.exception(ex)
                return Response({}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class DomobIosWall(generics.CreateAPIView):

    serializer_class = serializers.ScoreWallRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        service = FreebieService(request.service_repositories, request.activity_repository)
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            response = service.process_ios_domob_wall_order(request.user.id, **serializer.data)
            response_serializer = serializers.ScoreWallResponse(response)
            return Response(response_serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class LimeiIosWall(generics.CreateAPIView):

    serializer_class = serializers.ScoreWallRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        service = FreebieService(request.service_repositories, request.activity_repository)
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            response = service.process_ios_limei_wall_order(request.user.id, **serializer.data)
            response_serializer = serializers.ScoreWallResponse(response)
            return Response(response_serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)