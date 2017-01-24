from rest_framework import serializers

from django.conf import settings

STATUS_CHOICES = (
    (settings.ACCEPTED, settings.ACCEPTED),
    (settings.DECLINED, settings.DECLINED))

class FriendProfile(serializers.Serializer):
    user_id = serializers.IntegerField(source='user_id', read_only=True)
    gender = serializers.IntegerField(read_only=True)
    nick_name = serializers.CharField(read_only=True)
    avatar_url = serializers.CharField(read_only=True)
    currency = serializers.IntegerField(read_only=True)
    vip_title = serializers.IntegerField(read_only=True)
    total_win_rounds = serializers.IntegerField(read_only=True)
    total_lose_rounds = serializers.IntegerField(read_only=True)
    max_hand_card = serializers.CharField(read_only=True)
    gift_count = serializers.IntegerField(read_only=True)
    is_gaming = serializers.BooleanField(read_only=True)
    signature = serializers.CharField(read_only=True)

class MakeFriendRequest(serializers.Serializer):
    target_user_id = serializers.IntegerField(min_value=1)
    gift_id = serializers.IntegerField(min_value=1)

class ReplyFriendRequest(serializers.Serializer):
    target_user_id = serializers.IntegerField(min_value=1)
    request_id = serializers.IntegerField(min_value=1)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)

class BreakFriendship(serializers.Serializer):
    target_user_id = serializers.IntegerField(min_value=1, source='friend_user_id')

class SendCurrencyRequest(serializers.Serializer):
    target_user_id = serializers.IntegerField(min_value=1)
    currency = serializers.IntegerField(min_value=1)

class SendGiftRequest(serializers.Serializer):
    target_user_id = serializers.IntegerField(min_value=1)
    item_id = serializers.IntegerField(min_value=1)
    count = serializers.IntegerField(min_value=1)     

class FriendSendMessage(serializers.Serializer):
    target_user_id = serializers.IntegerField(min_value=1)
    messages = serializers.CharField(min_length=1, max_length=100)
        
class SendResponse(serializers.Serializer):
    currency = serializers.IntegerField()