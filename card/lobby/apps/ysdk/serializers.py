from rest_framework import serializers


class ChargeNotifyRequest(serializers.Serializer):
    openid = serializers.CharField()
    appid = serializers.CharField()
    ts = serializers.CharField()
    payitem = serializers.CharField()
    token = serializers.CharField()
    billno = serializers.CharField()
    version = serializers.CharField()
    zoneid = serializers.CharField()
    providetype = serializers.CharField()
    amt = serializers.CharField()
    payamt_coins = serializers.CharField()
    pubacct_payamt_coins = serializers.CharField()
    appmeta = serializers.CharField()
    clientver = serializers.CharField()
    sig = serializers.CharField()


class CreateOrderRequest(serializers.Serializer):
    open_id=serializers.CharField()
    open_key=serializers.CharField()
    pf=serializers.CharField()
    pf_key=serializers.CharField()
    channel_id = serializers.CharField()
    item_id = serializers.IntegerField()

class CreateOrderRequestPayM(serializers.Serializer):
    channel_id = serializers.CharField()
    item_id = serializers.IntegerField()

class CreateOrderResponse(serializers.Serializer):
    order_id = serializers.CharField()
    order_info = serializers.CharField()

class ChargeNotifyRequestPayM(serializers.Serializer):
    open_id = serializers.CharField()
    open_key = serializers.CharField()
    pf = serializers.CharField()
    pfkey = serializers.CharField()
    pay_token = serializers.CharField()
    transid = serializers.CharField()
    item_id = serializers.IntegerField()
