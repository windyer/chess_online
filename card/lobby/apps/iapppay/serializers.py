from rest_framework import serializers

class ChargeNotifyRequest(serializers.Serializer):
    transdata = serializers.CharField(max_length=3000)
    sign = serializers.CharField(max_length=500)
    signtype = serializers.CharField(max_length=20, required=False)

class CreateOrderRequest(serializers.Serializer):
    item_id = serializers.IntegerField()
    channel_id = serializers.CharField()

class CreateNormalOrderRequest(serializers.Serializer):
    item_id = serializers.IntegerField()
    channel_id = serializers.CharField()
    app_id = serializers.CharField()