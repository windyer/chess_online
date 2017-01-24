from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

import go.logging
from card.lobby.aop.logging import trace_view
from card.lobby.aop import api_view_available

from card.lobby import permissions
from card.lobby.apps.chat.serializers import ChatServer
from card.lobby.apps.chat.service import ChatService

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'login-chat':  reverse('login-chat', request=request, format=format)
        })

@go.logging.class_wrapper
class LoginChat(generics.CreateAPIView):

    serializer_class = ChatServer
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    def post(self, request, format=None):
        service = ChatService(request.service_repositories, 
                                request.activity_repository)
        chat_token = service.login_chat(request.user.id)
        serializer = self.get_serializer(chat_token)
        return Response(serializer.data)
