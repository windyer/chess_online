from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

import go.logging
from card.lobby.aop.logging import trace_view
from card.lobby.aop import request_limit, api_view_available
from card.lobby import permissions
import serializers
from .service import FriendService


@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'friends': reverse('friends', request=request, format=format),
        'request': reverse('request', request=request, format=format),
        'reply': reverse('reply', request=request, format=format),
        'break': reverse('break', request=request, format=format),
        'send-currency': reverse('send-currency', request=request, format=format),
        'send-gift': reverse('send-gift', request=request, format=format),
        'recommand': reverse('recommand', request=request, format=format),
        'send-message': reverse('send-message', request=request, format=format)
    })


@go.logging.class_wrapper
class FriendList(generics.ListAPIView):

    serializer_class = serializers.FriendProfile
    permission_classes = (permissions.IsPlayer,)
    paginate_by = 20
    paginate_by_param = 'page_size'

    def get_queryset(self):
        service = FriendService(self.request.service_repositories, 
                                self.request.activity_repository)
        query_set = service.get_friend_list(self.request.user.id)
        return query_set

    def get(self, request, format=None):
        return super(FriendList, self).get(request, format)


@go.logging.class_wrapper
class MakeFriendRequest(generics.CreateAPIView):

    serializer_class = serializers.MakeFriendRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    @request_limit(serializers.MakeFriendRequest)
    def post(self, request, format=None):
        service = FriendService(request.service_repositories, 
                                self.request.activity_repository)
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            response = service.make_friend(request.user.id, **serializer.data)
            response_serializer = serializers.SendResponse(response)
            return Response(response_serializer.data)
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class ReplyFriendRequest(generics.CreateAPIView):

    serializer_class = serializers.ReplyFriendRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    @request_limit(serializers.ReplyFriendRequest)
    def post(self, request, format=None):
        service = FriendService(request.service_repositories, 
                                self.request.activity_repository)
        serializer = self.get_serializer(data=request.DATA)
        
        if serializer.is_valid():
            service.reply_request(request.user.id, **serializer.data)
            return Response({})
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class BreakFriendship(generics.CreateAPIView):

    serializer_class = serializers.BreakFriendship
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    @request_limit(serializers.BreakFriendship)
    def post(self, request, format=None):
        service = FriendService(request.service_repositories, 
                                self.request.activity_repository)
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            request_status = service.break_friendship(request.user.id, **serializer.data)
            serializer = self.get_serializer(request_status)
            return Response(serializer.data)
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class FriendSendCurrency(generics.CreateAPIView):

    serializer_class = serializers.SendCurrencyRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    @request_limit(serializers.SendCurrencyRequest)
    def post(self, request, format=None):
        service = FriendService(request.service_repositories, 
                                self.request.activity_repository)
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            response = service.send_currency(request.user.id, **serializer.data)
            response_serializer = serializers.SendResponse(response)
            return Response(response_serializer.data)
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@go.logging.class_wrapper
class FriendSendGift(generics.CreateAPIView):

    serializer_class = serializers.SendGiftRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    @request_limit(serializers.SendGiftRequest)
    def post(self, request, format=None):
        service = FriendService(request.service_repositories, 
                                self.request.activity_repository)
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            response = service.send_gift(request.user.id, **serializer.data)
            response_serializer = serializers.SendResponse(response)
            return Response(response_serializer.data)
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class RecommandFriends(generics.ListAPIView):

    serializer_class = serializers.FriendProfile
    permission_classes = (permissions.IsPlayer,)
    paginate_by = 10
    paginate_by_param = 'page_size'

    def get_queryset(self):
        service = FriendService(self.request.service_repositories, 
                                self.request.activity_repository)
        query_set = service.get_recommand_friend(self.request.user.id)
        return query_set

    @trace_view
    def get(self, request, format=None):
        return super(RecommandFriends, self).get(request, format)



@go.logging.class_wrapper
class FriendSendMessage(generics.CreateAPIView):
 
    serializer_class = serializers.FriendSendMessage
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    @request_limit(serializers.FriendSendMessage)
    def post(self, request, format=None):
        service = FriendService(request.service_repositories, 
                                self.request.activity_repository)
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            status = service.send_message(request.user.id, **serializer.data)
            return Response({})
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
