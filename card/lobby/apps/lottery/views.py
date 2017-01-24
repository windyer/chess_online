from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

import go.logging

from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available

from card.lobby.apps.store.serializers import PurchaseResponse
from card.lobby import permissions
import serializers
from .service import LotteryService

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'item': reverse('item', request=request, format=format),
        'phone': reverse('phone', request=request, format=format),
        'qq': reverse('qq', request=request, format=format),
        'latest': reverse('latest', request=request, format=format),
        })

@go.logging.class_wrapper
class LotteryItem(generics.CreateAPIView):

    serializer_class = serializers.LotteryItem
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        service = LotteryService(request.service_repositories, 
                                request.activity_repository)
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            response = service.lottery_item(request.user.id, **serializer.data)
            return Response(response)
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class LotteryPhone(generics.CreateAPIView):

    serializer_class = serializers.LotteryPhone
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        service = LotteryService(request.service_repositories, 
                                request.activity_repository)
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            response = service.lottery_phone(request.user.id, **serializer.data)
            return Response(response)
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@go.logging.class_wrapper
class LotteryQQ(generics.CreateAPIView):

    serializer_class = serializers.LotteryQQ
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        service = LotteryService(request.service_repositories, 
                                request.activity_repository)
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            response = service.lottery_qq(request.user.id, **serializer.data)
            return Response(response)
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class LotteryLatest(generics.RetrieveAPIView, generics.CreateAPIView):
    serializer_class = serializers.LotteryItem
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def get(self, request, format=None):
        service = LotteryService(request.service_repositories, 
                                request.activity_repository)
        response = service.get_latest_exchage()
        return Response(response)