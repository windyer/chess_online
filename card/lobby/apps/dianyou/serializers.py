from rest_framework import serializers

class Login(serializers.Serializer):
    session = serializers.CharField()

class ChargeNotifyRequest(serializers.Serializer):
    app = serializers.CharField()
    cbi = serializers.CharField()
    ct = serializers.IntegerField()
    fee = serializers.IntegerField()
    pt = serializers.IntegerField()
    sdk = serializers.CharField()
    ssid = serializers.CharField()
    st = serializers.IntegerField()
    tcd = serializers.CharField()
    uid = serializers.CharField()
    ver = serializers.CharField()
    sign = serializers.CharField()
class CreateOrderRequest(serializers.Serializer):
    item_id = serializers.IntegerField()
    channel_id = serializers.CharField()

class CreateOrderResponse(serializers.Serializer):
    order_id = serializers.CharField()
    order_info = serializers.CharField()