from rest_framework import serializers

class Login(serializers.Serializer):
    session = serializers.CharField()

class ChargeNotifyRequest(serializers.Serializer):
    cp_order_id = serializers.CharField()
    correlator = serializers.CharField()
    result_code = serializers.CharField()
    fee = serializers.IntegerField()
    pay_type = serializers.CharField()
    method= serializers.CharField()
    sign = serializers.CharField()
    version = serializers.CharField()

class CreateOrderRequest(serializers.Serializer):
    item_id = serializers.IntegerField()
    channel_id = serializers.CharField()

class CreateOrderResponse(serializers.Serializer):
    order_id = serializers.CharField()
    order_info = serializers.CharField()