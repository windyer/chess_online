from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

import go.logging

from card.lobby.aop.logging import trace_view
from card.lobby.aop import request_limit, api_view_available
from card.lobby import permissions

import serializers
from .service import TimeLineService

@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
            'system-message': reverse('system-message', request=request, format=format),
            'del-friend-message': reverse('del-friend-message', request=request, format=format),
            'unread-system-message': reverse('unread-system-message', request=request, format=format),
        })

@go.logging.class_wrapper
class FriendTrend(generics.ListAPIView):
    permission_classes = (permissions.IsPlayer,)
    
    def get(self, request, format=None, **kwargs):
        request_serializer = serializers.FriendTrendRequset(data=kwargs)
        if request_serializer.is_valid():
            timeline_servcie = TimeLineService(self.request.service_repositories, 
                                request.activity_repository)
            resp = timeline_servcie.get_friend_trends(self.request.user.id, **request_serializer.data)
            return Response(resp)
        else:
            from rest_framework import status
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class PersonalMessage(generics.ListAPIView):
    permission_classes = (permissions.IsPlayer,)
    
    def get(self, request, format=None, **kwargs):
        request_serializer = serializers.PersonalMessageRequset(data=kwargs)
        if request_serializer.is_valid():
            timeline_servcie = TimeLineService(self.request.service_repositories, 
                                request.activity_repository)
            resp = timeline_servcie.get_personal_message(self.request.user.id, **request_serializer.data)
            return Response(resp)
        else:
            from rest_framework import status
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class SystemMessage(generics.ListAPIView, generics.CreateAPIView, generics.DestroyAPIView):
    permission_classes = (permissions.IsPlayer,)
    serializer_class = serializers.SystemMessageRequest
    
    def get(self, request, format=None, **kwargs):
        timeline_servcie = TimeLineService(self.request.service_repositories, 
                            request.activity_repository)
        resp = timeline_servcie.get_system_message(self.request.user.id)
        return Response(resp)

@go.logging.class_wrapper
class FriendMessage(generics.ListAPIView):
    permission_classes = (permissions.IsPlayer,)
    
    def get(self, request, format=None, **kwargs):
        request_serializer = serializers.FriendMessageRequset(data=kwargs)
        if request_serializer.is_valid():
            timeline_servcie = TimeLineService(self.request.service_repositories, 
                                    request.activity_repository)
            resp = timeline_servcie.get_friend_messages(self.request.user.id, **request_serializer.data)
            return Response(resp)
        else:
            from rest_framework import status
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class DelFriendMessage(generics.CreateAPIView):
    serializer_class   = serializers.DelFriendMessageRequest
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    @request_limit(serializers.DelFriendMessageRequest)
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            timeline_servcie = TimeLineService(
                self.request.service_repositories, request.activity_repository)
            user_id = request.user.id
            timeline_servcie.delete_friend_message(user_id, **serializer.data)
            return Response({})
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class SystemPush(generics.ListAPIView):
    
    def get(self, request, format=None, **kwargs):
        request_serializer = serializers.SystemPushRequest(data=kwargs)
        
        if request_serializer.is_valid():
            timeline_servcie = TimeLineService(self.request.service_repositories, 
                                request.activity_repository)
            resp = timeline_servcie.get_system_push(**request_serializer.data)
            serializer = self.get_serializer(resp)
            return Response(serializer.data)
        else:
            from rest_framework import status
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class UnreadSystemMessage(generics.ListAPIView):

    def get(self, request, format=None, **kwargs):
        request_serializer = serializers.UnreadSystemMessageRequest(data=kwargs)
        
        if request_serializer.is_valid():
            timeline_servcie = TimeLineService(self.request.service_repositories, 
                                request.activity_repository)
            user_id = request.user.id
            resp = timeline_servcie.get_system_message_unread_info(**request_serializer.data)
            resp['disable_encoder'] = True
            return Response(resp)
        else:
            from rest_framework import status
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
