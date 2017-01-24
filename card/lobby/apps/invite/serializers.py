from rest_framework import serializers

class InfoRequest(serializers.Serializer):
    user_id = serializers.IntegerField()

class AwardRequest(serializers.Serializer):
    item_id = serializers.IntegerField()
    channel_id = serializers.CharField()

class SedInviterRequest(serializers.Serializer):
    user_id = serializers.IntegerField()
    inviter_id = serializers.IntegerField()