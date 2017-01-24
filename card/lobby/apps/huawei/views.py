from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.http import HttpResponse

import go.logging

from card.lobby import permissions
from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available
from card.lobby.apps.huawei.service import HuaweiService
from card.lobby.apps.huawei import serializers
from django.conf import settings

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'create_order': reverse('create-order', request=request, format=format),
        'charge_notify': reverse('charge-notify', request=request, format=format),
    })

@go.logging.class_wrapper
class CreateOrder(generics.CreateAPIView):

    serializer_class = serializers.CreateOrderRequest
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = HuaweiService(self.request.service_repositories, self.request.activity_repository)
            resp = service.create_charge_order(request.user.id, **serializer.data)
            return Response(resp)
        else:
            return Response(serializer.errors)

@go.logging.class_wrapper
class ChargeNotify(generics.CreateAPIView):

    serializer_class = serializers.ChargeNotifyRequest

    @trace_view
    def post(self, request, format=None):

        try:
            data = request.DATA
            data = dict(data)
            sign = data.pop("sign")[0]
            if 'signType' in data:
                data.pop('signType')
            requestId = data['requestId'][0]
            dic_data={}
            for i  in data:
                dic_data[i] = data[i][0]
            service = HuaweiService(self.request.service_repositories, self.request.activity_repository)
            resp = service.process_charge_order(dic_data,requestId,sign)
            return HttpResponse(resp, content_type="text/plain")
        except:
            return HttpResponse("FAILURE", content_type="text/plain")
