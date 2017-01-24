from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.http import HttpResponse

import go.logging

from card.lobby import permissions
from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available
from card.lobby.apps.wiipay.service import WiiPayService
from card.lobby.apps.wiipay import serializers
from django.conf import settings

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'order/create': reverse('wiipay-order-create', request=request, format=format),
        'order/notify_zx001': reverse('wiipay-order-notify-zx001', request=request, format=format),
        'order/notify_zx002': reverse('wiipay-order-notify-zx002', request=request, format=format),
    })

@go.logging.class_wrapper
class CreateOrder(generics.CreateAPIView):

    serializer_class = serializers.CreateOrderRequest
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = WiiPayService(self.request.service_repositories, self.request.activity_repository)
            resp = service.create_charge_order(request.user.id,  **serializer.data)
            return Response(resp)
        else:
            return Response(serializer.errors)

@go.logging.class_wrapper
class ChargeNotify(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = WiiPayService(self.request.service_repositories, self.request.activity_repository)
            request_body = "request.body"
            resp = service.process_charge_order(request_body=request_body, app_id=settings.WIIPAY.appid_wiipay_pay, **serializer.data)
            return HttpResponse(resp, content_type="text/plain")
        else:
            return HttpResponse("FAILURE", content_type="text/plain")

@go.logging.class_wrapper
class ChargeNotify_ZX002(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = WiiPayService(self.request.service_repositories, self.request.activity_repository)
            request_body = "request.body"
            resp = service.process_charge_order(request_body=request_body, app_id=settings.WIIPAY.appid_zx002_pay, **serializer.data)
            return HttpResponse(resp, content_type="text/plain")
        else:
            return HttpResponse("FAILURE", content_type="text/plain")

