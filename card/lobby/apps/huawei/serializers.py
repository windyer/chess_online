from rest_framework import serializers

class ChargeNotifyRequest(serializers.Serializer):
    result = serializers.CharField()
    userName = serializers.CharField()
    productName = serializers.CharField()
    payType = serializers.IntegerField()
    amount = serializers.CharField()
    orderId = serializers.CharField()
    notifyTime = serializers.CharField()
    requestId = serializers.CharField()
    sign = serializers.CharField()


class CreateOrderRequest(serializers.Serializer):
    item_id = serializers.IntegerField()
    channel_id = serializers.CharField()
