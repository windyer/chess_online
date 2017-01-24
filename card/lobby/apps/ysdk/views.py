from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.http import HttpResponse

import go.logging

from card.lobby import permissions
from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available
from card.lobby.apps.ysdk.service import YsdkService
from card.lobby.apps.ysdk import serializers
import operator
import urllib
import json

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'create-order': reverse('create-order', request=request, format=format),
        'charge-notify': reverse('charge-notify', request=request, format=format),
    })

@go.logging.class_wrapper
class CreateOrder(generics.CreateAPIView):

    serializer_class = serializers.CreateOrderRequest
    #permission_classes = (permissions.IsPlayer,)

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = YsdkService(self.request.service_repositories, self.request.activity_repository)
            user_id = request.user.id
            resp = service.create_charge_order(user_id, **serializer.data)
            return Response(resp)
        else:
            return Response(serializer.errors)

@go.logging.class_wrapper
class CreateOrderPayM(generics.CreateAPIView):

    serializer_class = serializers.CreateOrderRequestPayM
    #permission_classes = (permissions.IsPlayer,)

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = YsdkService(self.request.service_repositories, self.request.activity_repository)
            user_id = request.user.id
            resp = service.create_charge_order_pay_m(user_id, **serializer.data)
            return Response(resp)
        else:
            return Response(serializer.errors)

@go.logging.class_wrapper
class ChargeNotify(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def get(self, request, format=None):
        try:
            '''
            data = request.REQUEST
            openid=data['openid']
            appid=data['appid']
            ts=data['ts']
            payitem = data['payitem']
            token = data['token']
            billno =data['billno']
            version =data['version']
            zoneid =data['zoneid']
            providetype =data['providetype']
            amt=data['amt']
            payamt_coins=data['payamt_coins']
            pubacct_payamt_coins=data['pubacct_payamt_coins']
            appmeta=data['appmeta']
            clientver=data['clientver']
            sig=data['sig']
            serializer = self.get_serializer(data=request.GET)
            '''
            params = request.GET.dict()
            url_path=request.path
            service = YsdkService(self.request.service_repositories, self.request.activity_repository)
            resp = service.process_charge_order(url_path,params)
            return HttpResponse(resp)
        except Exception:
            return HttpResponse(json.dumps({"ret":1,"msg":"failed"}))

@go.logging.class_wrapper
class ChargeNotifyPayM(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequestPayM

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = YsdkService(self.request.service_repositories, self.request.activity_repository)
            user_id = request.user.id
            resp = service.process_charge_order_pay_m(user_id, **serializer.data)
            return Response(resp)
        else:
            return Response(serializer.errors)