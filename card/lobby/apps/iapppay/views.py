from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.http import HttpResponse

import go.logging

from card.lobby import permissions
from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available
from card.lobby.apps.iapppay.service import IAppPayService
from card.lobby.apps.iapppay import serializers
from django.conf import settings

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'order/create': reverse('iapppay-order-create', request=request, format=format),
        'order/notify': reverse('iapppay-order-notify', request=request, format=format),
        'order/create_holytree': reverse('iapppay-order-create-holytree', request=request, format=format),
        'order/notify_holytree': reverse('iapppay-order-notify-holytree', request=request, format=format),
        'order/create_zx': reverse('iapppay-order-create-zx', request=request, format=format),
        'order/notify_zx': reverse('iapppay-order-notify-zx', request=request, format=format),
        'order/create_zx003': reverse('iapppay-order-create-zx003', request=request, format=format),
        'order/notify_zx003': reverse('iapppay-order-notify-zx003', request=request, format=format),
        'order/create_zx010': reverse('iapppay-order-create-zx010', request=request, format=format),
        'order/notify_zx010': reverse('iapppay-order-notify-zx010', request=request, format=format),
        'order/create_order': reverse('iapppay-order-create-order', request=request, format=format),
        'order/notify_sj04': reverse('iapppay-order-notify-sj04', request=request, format=format),
        'order/notify_lenovo': reverse('iapppay-order-notify-lenovo-duowan', request=request, format=format),
        'order/notify_fg': reverse('iapppay-order-notify-fg', request=request, format=format),
        'order/notify_sj': reverse('iapppay-order-notify-sj', request=request, format=format),
        'order/notify_hy': reverse('iapppay-order-notify-hy', request=request, format=format),
        'order/notify_ly_qmzjh': reverse('iapppay-order-notify-ly-qmzjh', request=request, format=format),
    })

@go.logging.class_wrapper
class CreateOrder(generics.CreateAPIView):

    serializer_class = serializers.CreateOrderRequest
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            resp = service.create_normal_charge_order(request.user.id, settings.IAPPPAY.appid_iapp_pay, **serializer.data)
            #if resp['limit'] == 0:
                #return Response(status=411004)
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
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            request_body = "request.body"
            resp = service.process_normal_charge_order(request_body=request_body, app_id=settings.IAPPPAY.appid_iapp_pay, **serializer.data)
            return HttpResponse(resp, content_type="text/plain")
        else:
            return HttpResponse("FAILURE", content_type="text/plain")

@go.logging.class_wrapper
class CreateOrderHolytree(generics.CreateAPIView):

    serializer_class = serializers.CreateOrderRequest
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            resp = service.create_normal_charge_order(request.user.id, settings.IAPPPAY.appid_holytree_pay, **serializer.data)
            return Response(resp)
        else:
            return Response(serializer.errors)

@go.logging.class_wrapper
class ChargeNotifyHolytree(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            request_body = "request.body"
            resp = service.process_normal_charge_order(request_body=request_body, app_id=settings.IAPPPAY.appid_holytree_pay, **serializer.data)
            return HttpResponse(resp, content_type="text/plain")
        else:
            return HttpResponse("FAILURE", content_type="text/plain")

@go.logging.class_wrapper
class CreateOrderZX(generics.CreateAPIView):

    serializer_class = serializers.CreateOrderRequest
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            resp = service.create_normal_charge_order(request.user.id, settings.IAPPPAY.appid_zx_pay, **serializer.data)
            return Response(resp)
        else:
            return Response(serializer.errors)

@go.logging.class_wrapper
class ChargeNotifyZX(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            request_body = "request.body"
            resp = service.process_normal_charge_order(request_body=request_body, app_id=settings.IAPPPAY.appid_zx_pay, **serializer.data)
            return HttpResponse(resp, content_type="text/plain")
        else:
            return HttpResponse("FAILURE", content_type="text/plain")

@go.logging.class_wrapper
class CreateOrderZX003(generics.CreateAPIView):

    serializer_class = serializers.CreateOrderRequest
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            resp = service.create_normal_charge_order(request.user.id, settings.IAPPPAY.appid_zx003_pay, **serializer.data)
            return Response(resp)
        else:
            return Response(serializer.errors)

@go.logging.class_wrapper
class ChargeNotifyZX003(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            request_body = "request.body"
            resp = service.process_normal_charge_order(request_body=request_body, app_id=settings.IAPPPAY.appid_zx003_pay, **serializer.data)
            return HttpResponse(resp, content_type="text/plain")
        else:
            return HttpResponse("FAILURE", content_type="text/plain")

@go.logging.class_wrapper
class CreateOrderZX010(generics.CreateAPIView):

    serializer_class = serializers.CreateOrderRequest
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            resp = service.create_normal_charge_order(request.user.id, settings.IAPPPAY.appid_zx010_pay, **serializer.data)
            return Response(resp)
        else:
            return Response(serializer.errors)

@go.logging.class_wrapper
class ChargeNotifyZX010(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            request_body = "request.body"
            resp = service.process_normal_charge_order(request_body=request_body, app_id=settings.IAPPPAY.appid_zx010_pay, **serializer.data)
            return HttpResponse(resp, content_type="text/plain")
        else:
            return HttpResponse("FAILURE", content_type="text/plain")

@go.logging.class_wrapper
class CreateNormalOrder(generics.CreateAPIView):

    serializer_class = serializers.CreateNormalOrderRequest
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            resp = service.create_normal_charge_order(request.user.id, **serializer.data)
            return Response(resp)
        else:
            return Response(serializer.errors)

@go.logging.class_wrapper
class ChargeNotifySJ04(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            request_body = "request.body"
            resp = service.process_normal_charge_order(request_body=request_body, app_id=settings.IAPPPAY.appid_sj04_pay, **serializer.data)
            return HttpResponse(resp, content_type="text/plain")
        else:
            return HttpResponse("FAILURE", content_type="text/plain")

@go.logging.class_wrapper
class ChargeNotifyLenovo(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            request_body = "request.body"
            resp = service.process_normal_charge_order(request_body=request_body, app_id=settings.IAPPPAY.appid_lenovo_duowan, **serializer.data)
            return HttpResponse(resp, content_type="text/plain")
        else:
            return HttpResponse("FAILURE", content_type="text/plain")

@go.logging.class_wrapper
class ChargeNotifyFG(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            request_body = "request.body"
            resp = service.process_normal_charge_order(request_body=request_body, app_id=settings.IAPPPAY.appid_fg_pay, **serializer.data)
            return HttpResponse(resp, content_type="text/plain")
        else:
            return HttpResponse("FAILURE", content_type="text/plain")

@go.logging.class_wrapper
class ChargeNotifySJ(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            request_body = "request.body"
            resp = service.process_normal_charge_order(request_body=request_body, app_id=settings.IAPPPAY.appid_sj_pay, **serializer.data)
            return HttpResponse(resp, content_type="text/plain")
        else:
            return HttpResponse("FAILURE", content_type="text/plain")

@go.logging.class_wrapper
class ChargeNotifyHY(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            request_body = "request.body"
            resp = service.process_normal_charge_order(request_body=request_body, app_id=settings.IAPPPAY.appid_hy_pay, **serializer.data)
            return HttpResponse(resp, content_type="text/plain")
        else:
            return HttpResponse("FAILURE", content_type="text/plain")

@go.logging.class_wrapper
class ChargeNotifyLYQMZJH(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = IAppPayService(self.request.service_repositories, self.request.activity_repository)
            request_body = "request.body"
            resp = service.process_normal_charge_order(request_body=request_body, app_id=settings.IAPPPAY.appid_ly_qmzjh_pay, **serializer.data)
            return HttpResponse(resp, content_type="text/plain")
        else:
            return HttpResponse("FAILURE", content_type="text/plain")