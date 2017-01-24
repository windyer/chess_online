from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.http import HttpResponse

import go.logging

from card.lobby import permissions
from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available
from card.lobby.apps.moguwan.service import MoguwanService
from card.lobby.apps.moguwan import serializers
import operator
import urllib

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
            service = MoguwanService(self.request.service_repositories, self.request.activity_repository)
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
            service = MoguwanService(self.request.service_repositories, self.request.activity_repository)
            resp = service.create_charge_order(request.user.id, **serializer.data)
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
            service = MoguwanService(self.request.service_repositories, self.request.activity_repository)
            resp = service.process_charge_order(request.user.id, **serializer.data)
            return HttpResponse(resp, content_type="text/plain")
        else:
            return HttpResponse("FAILURE", content_type="text/plain")
