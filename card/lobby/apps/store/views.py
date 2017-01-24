from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from card.core.property.three import Property
import go.logging
from django.http import HttpResponse
from card.core.charge import ITEMS
from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available
from card.lobby import permissions

import serializers
from .service import StoreService

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'purchase': reverse('purchase-item', request=request, format=format),
        'sell': reverse('sell-item', request=request, format=format),
        'bull-url': reverse('bull-url', request=request, format=format),
        'store-item': reverse('store-item', request=request, format=format),
        'bull-complete': reverse('bull-complete', request=request, format=format),
        })

@go.logging.class_wrapper
class PurchaseItem(generics.CreateAPIView):

    serializer_class = serializers.PurchaseItem
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        service    = StoreService(request.service_repositories, 
                                request.activity_repository)
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            item_id = serializer.data['item_id']
            response = service.purchase_item(request.user.id, **serializer.data)
            response_serializer = serializers.PurchaseResponse(response._asdict())
            response_serializer.data['item_id'] =item_id
            return Response(response_serializer.data)
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@go.logging.class_wrapper
class SellItem(generics.CreateAPIView):

    serializer_class   = serializers.SellItem
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        service = StoreService(request.service_repositories, 
                                request.activity_repository)
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            item_id = serializer.data['item_id']
            response = service.sell_item(request.user.id, **serializer.data)
            response_serializer = serializers.SellResponse(response._asdict())
            response_serializer.data['item_id'] =item_id
            return Response(response_serializer.data)

        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@go.logging.class_wrapper
class BullUrl(generics.ListAPIView):

    serializer_class   = serializers.BullUrl
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def get(self, request, format=None):
        service = StoreService(request.service_repositories, 
                                request.activity_repository)
        response = service.get_bull_url(request.user.id)
        return Response(response)

@go.logging.class_wrapper
class BullComplete(generics.ListAPIView):

    serializer_class   = serializers.BullUrl
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def get(self, request, format=None):
        service = StoreService(request.service_repositories, 
                                request.activity_repository)
        response = service.bull_complete(request.user.id)
        return Response({})


@go.logging.class_wrapper
class StoreItem(generics.CreateAPIView):

    serializer_class   = serializers.StoreItem
    #permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def get(self, request, format=None):
        resp = {}
        for item_id in ITEMS.coins:
            item = ITEMS.coins[item_id]
            resp[item_id.item_id] = item.cat_food
        resp['751'] = 288/2
        return Response(resp)
