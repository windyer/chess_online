from rest_framework import serializers

class Login(serializers.Serializer):
    session = serializers.CharField()

class ChargeNotifyRequest(serializers.Serializer):
    #appid = serializers.IntegerField()
    #from = serializers.CharField()
    tradeSuccessTime = serializers.CharField()
    userId = serializers.CharField()
    sign = serializers.CharField()
    result = serializers.CharField()
    tradeNo = serializers.CharField()
    notifyTime = serializers.CharField()
    tradeService = serializers.CharField()
    tradeCreateTime = serializers.CharField()
    charset = serializers.CharField()
    attach = serializers.CharField()
    tradeName = serializers.CharField()
    sellerId = serializers.CharField()
    tradeStatus = serializers.CharField()
    utradeDesc = serializers.CharField()
    totalFee = serializers.IntegerField()
    timestamp = serializers.IntegerField()
    paymentType = serializers.CharField()
    cashFee = serializers.IntegerField()
    appkey = serializers.CharField()
    settleFee = serializers.IntegerField()
    signType = serializers.CharField()
    apiVersion = serializers.CharField()
    transactionId = serializers.CharField()
    notifyId = serializers.CharField()



class CreateOrderRequest(serializers.Serializer):
    item_id = serializers.IntegerField()
    channel_id = serializers.CharField()

class CreateOrderResponse(serializers.Serializer):
    order_id = serializers.CharField()
    order_info = serializers.CharField()