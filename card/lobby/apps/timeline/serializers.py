from rest_framework import serializers

from card.lobby.apps.rank.serializers import PersonalRanks

class EventSenderProfile(serializers.Serializer):
    user_id = serializers.IntegerField()
    nick_name = serializers.CharField()
    currency = serializers.IntegerField()
    ranks = PersonalRanks(many=False, required=False)
    avatar_url = serializers.CharField(required=False)

class FriendMessageRequset(serializers.Serializer):
    peer_user_id = serializers.IntegerField(min_value=1)
    page = serializers.IntegerField(min_value=1) 

class FriendTrendRequset(serializers.Serializer):
    page = serializers.IntegerField(min_value=1) 

class PersonalMessageRequset(serializers.Serializer):
    page = serializers.IntegerField(min_value=1) 
    
class TimeLineUnread(serializers.Serializer):
    pass

class DelFriendMessageRequest(serializers.Serializer):
    peer_user_id = serializers.IntegerField(min_value=1)

class SystemMessageRequest(serializers.Serializer):
    message = serializers.CharField(min_length=1, max_length=24)
    is_top = serializers.BooleanField()

class SystemPushRequest(serializers.Serializer):
    device_id = serializers.CharField(min_length=1, max_length=50)
    
class UreadEventCount(serializers.Serializer):
    friend_trend = serializers.IntegerField()
    friend_message = serializers.IntegerField()
    personal_message = serializers.IntegerField()
    system_message = serializers.IntegerField()

class UnreadSystemMessageRequest(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)