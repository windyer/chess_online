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
from .service import RouletteService

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'game': reverse('roulette-game', request=request, format=format),
        'record': reverse('roulette-record', request=request, format=format),
        'next-roulette-type': reverse('next-roulette-type', request=request, format=format),
        })

@go.logging.class_wrapper
class Roulette(generics.CreateAPIView):

    serializer_class = serializers.Roulette
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        service = RouletteService(request.service_repositories, 
                                request.activity_repository)
        (next_type, item_id, db_resp) = service.roulette(request.user.id)
        response_serializer = PurchaseResponse(db_resp._asdict())
        response_serializer.data['item_id'] =item_id
        response_serializer.data['next_type'] =next_type
        
        return Response(response_serializer.data)

@go.logging.class_wrapper
class RouletteRecord(generics.ListAPIView):

    serializer_class = serializers.RouletteRecord
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def get(self, request, format=None):
        service = RouletteService(self.request.service_repositories, 
                                request.activity_repository)
        query_set = service.get_record(self.request.user.id)

        resp={}
        for item in query_set:
            resp[item.item_id] = item.item_count

        return Response(resp)

@go.logging.class_wrapper
class NextRouletteType(generics.ListAPIView):

    serializer_class = serializers.NextRouletteType
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def get(self, request, format=None):
        service = RouletteService(self.request.service_repositories, 
                                request.activity_repository)
        next_type = service.get_next_roulette_type(self.request.user.id)
        resp = {"next_roulette_type":next_type}
        serializer = self.get_serializer(resp)
        return Response(serializer.data)
