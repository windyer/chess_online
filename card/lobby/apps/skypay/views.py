from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

import go.logging
from card.lobby.aop.logging import trace_view
from card.lobby.aop import request_limit, api_view_available
from card.lobby import permissions
from card.lobby.apps.skypay.service import SkyPayService
from card.lobby.apps.skypay import serializers

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'order/create': reverse('order-create', request=request, format=format),
        'order/notify': reverse('order-notify', request=request, format=format),
    })

@go.logging.class_wrapper
class ChargeNotify(generics.ListAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def get(self, request, format=None):
        serializer = self.get_serializer(data=dict(request.QUERY_PARAMS.iteritems()))
        if serializer.is_valid():
            query_string = request.META['QUERY_STRING']
            service = SkyPayService(self.request.service_repositories, self.request.activity_repository)
            resp = service.process_charge_order(query_string=query_string, **serializer.data)
            return Response(resp)
        else:
            return Response("result={0}".format(1))

@go.logging.class_wrapper
class CreateOrder(generics.CreateAPIView):

    serializer_class = serializers.CreateOrderRequest
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = SkyPayService(self.request.service_repositories, self.request.activity_repository)
            resp = service.create_charge_order(request.user.id, **serializer.data)
            return Response(resp)
        else:
            return Response(serializer.errors)