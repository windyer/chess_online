from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.http import HttpResponseRedirect
import go.logging
from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available
import datetime
from card.lobby.extensions.logging import mongo_logger
@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'landpage':  reverse('landpage', request=request, format=format),
        })

@go.logging.class_wrapper
class LandPage(generics.CreateAPIView):
    @trace_view
    def get(self, request, format=None):
        data = request.REQUEST
        time = datetime.date.today()
        return HttpResponseRedirect('')