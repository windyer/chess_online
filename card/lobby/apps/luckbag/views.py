from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
import go.logging
from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available
from card.lobby.apps.luckbag import serializers
from card.lobby.apps.luckbag.service import LuckbagService
import time
import ujson
@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'open_bag':  reverse('open_bag', request=request, format=format),
        })

@go.logging.class_wrapper
class LuckBag(generics.CreateAPIView):
    serializer_class = serializers.Post

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = LuckbagService(self.request.service_repositories, self.request.activity_repository)
            response = service.luckbag(**serializer.data)
            return Response(response)
        else:
            return Response(serializer.errors)

    @trace_view
    def get(self, request, format=None):
        service = LuckbagService(self.request.service_repositories, self.request.activity_repository)
        user_id = request.user.id
        click_time = str(time.time())
        response = service.luckbag(user_id,click_time)
        #response = ujson.dumps(response)
        return Response(response)