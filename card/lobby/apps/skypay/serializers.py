from rest_framework import serializers

class ChargeNotifyRequest(serializers.Serializer):
    orderId = serializers.CharField(max_length=60)
    cardType = serializers.CharField(max_length=20)
    skyId = serializers.IntegerField()
    resultCode = serializers.IntegerField()
    payNum = serializers.CharField(max_length=60)
    realAmount = serializers.IntegerField()
    payTime = serializers.CharField(max_length=20)
    failure = serializers.CharField(max_length=20)
    failDesc = serializers.CharField(max_length=300, required=False)
    ext1 = serializers.CharField(max_length=50, required=False)
    ext2 = serializers.CharField(max_length=50, required=False)
    ext3 = serializers.CharField(max_length=50, required=False)
    signMsg = serializers.CharField(max_length=40)

class CreateOrderRequest(serializers.Serializer):
    item_id = serializers.IntegerField()
    channel_id = serializers.CharField()
    version_code = serializers.IntegerField()
    non_sms = serializers.BooleanField(default=False)
    pay_type = serializers.IntegerField(required=False)
    order_skipTip = serializers.BooleanField(required=False)
    order_skipResult = serializers.BooleanField(required=False)
    skypay_method = serializers.CharField(required=False)

class CreateOrderResponse(serializers.Serializer):
    order_id = serializers.CharField()
    order_info = serializers.CharField()