from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.http import HttpResponse

import go.logging

from card.lobby import permissions
from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available
from card.lobby.apps.yuyang.service import YuYangService
from card.lobby.apps.yuyang import serializers
import operator
import urllib
import ujson
@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        #'login': reverse('login', request=request, format=format),
        'create-order': reverse('create-order', request=request, format=format),
        'charge-notify': reverse('charge-notify', request=request, format=format),
    })

@go.logging.class_wrapper
class Login(generics.CreateAPIView):

    serializer_class = serializers.Login
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = YuYangService(self.request.service_repositories, self.request.activity_repository)
            resp = service.login(**serializer.data)
            return Response(resp)
        else:
            return Response(serializer.errors)

@go.logging.class_wrapper
class CreateOrder(generics.CreateAPIView):

    serializer_class = serializers.CreateOrderRequest
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = YuYangService(self.request.service_repositories, self.request.activity_repository)
            resp = service.create_charge_order(request.user.id, **serializer.data)
            return Response(resp)
        else:
            return Response(serializer.errors)

@go.logging.class_wrapper
class ChargeNotify(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def post(self, request, *args, **kwargs):
        try:
            data = request.REQUEST
            game_id = data['game_id']
            cp_trade_no=data['cp_trade_no']
            uid = data['uid']
            total_fee=data['total_fee']
            pay_status = data['pay_status']
            sign = data['sign']
            service = YuYangService(self.request.service_repositories, self.request.activity_repository)
            resp = service.process_charge_order(game_id,cp_trade_no, uid, total_fee,pay_status,sign)

            return HttpResponse(ujson.dumps(resp), content_type="text/plain")
        except Exception:
            return HttpResponse("FAILURE", content_type="text/plain")
