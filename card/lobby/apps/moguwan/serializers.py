from rest_framework import serializers

class Login(serializers.Serializer):
    token = serializers.CharField()
    
class ChargeNotifyRequest(serializers.Serializer):
    out_trade_no = serializers.CharField()
    price = serializers.CharField()
    pay_status = serializers.CharField()
    extend = serializers.CharField()
    signType = serializers.CharField()
    sign = serializers.CharField()

class CreateOrderRequest(serializers.Serializer):
    item_id = serializers.IntegerField()
    channel_id = serializers.CharField()

class CreateOrderResponse(serializers.Serializer):
    order_id = serializers.CharField()
    order_info = serializers.CharField()