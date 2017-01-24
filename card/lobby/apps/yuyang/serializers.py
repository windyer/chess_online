from rest_framework import serializers

class Login(serializers.Serializer):
    session = serializers.CharField()

class ChargeNotifyRequest(serializers.Serializer):
    game_id = serializers.IntegerField()
    cp_trade_no = serializers.CharField()
    total_fee = serializers.IntegerField()
    uid = serializers.CharField()
   # jfd = serializers.CharField()
    pay_status = serializers.CharField()
   # paychannel = serializers.CharField()
   # phone = serializers.CharField()
   # channel = serializers.CharField()
    #from = serializers.CharField()
    sign = serializers.CharField()
   # extchannel = serializers.CharField()
   # cpdefinepart = serializers.CharField()


class CreateOrderRequest(serializers.Serializer):
    item_id = serializers.IntegerField()
    channel_id = serializers.CharField()

class CreateOrderResponse(serializers.Serializer):
    order_id = serializers.CharField()
    order_info = serializers.CharField()