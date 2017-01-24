from rest_framework import serializers
from django.conf import settings

TURNER_CHOICES = (
    (settings.TURNER.large, settings.TURNER.large),
    (settings.TURNER.small, settings.TURNER.small),
)

class TurnerBegin(serializers.Serializer):
    suit = serializers.CharField(read_only=True)
    rank = serializers.CharField(read_only=True)
    round = serializers.IntegerField(read_only=True)
    currency = serializers.IntegerField(read_only=True)

class TurnerGamingReponse(serializers.Serializer):
    suit = serializers.CharField()
    rank = serializers.CharField()
    round = serializers.IntegerField()
    status = serializers.CharField()
    currency = serializers.IntegerField()

class TurnerGamingRequest(serializers.Serializer):
    choice = serializers.ChoiceField(choices=TURNER_CHOICES)
    round = serializers.IntegerField(min_value=0, max_value=3)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                
class TurnerEndRequest(serializers.Serializer):
    pass

class TurnerEndReponse(serializers.Serializer):
    status = serializers.CharField()
    currency = serializers.IntegerField(read_only=True)