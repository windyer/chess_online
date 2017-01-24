from rest_framework import serializers

class ChargeNotifyRequest(serializers.Serializer):
    operatorType = serializers.CharField(max_length=3000)
    operatorTypeTile = serializers.CharField(max_length=500)
    channelCode = serializers.CharField(max_length=500)
    appCode = serializers.CharField(max_length=500)
    payCode = serializers.CharField(max_length=500)
    imsi = serializers.CharField(max_length=500)
    tel = serializers.CharField(max_length=500)
    state = serializers.CharField(max_length=500)
    bookNo = serializers.CharField(max_length=500)
    date = serializers.CharField(max_length=500)
    price = serializers.IntegerField()
    devPrivate = serializers.CharField(max_length=500)
    synType = serializers.CharField(max_length=500)
    sig = serializers.CharField(max_length=500)

class CreateOrderRequest(serializers.Serializer):
    item_id = serializers.IntegerField()
    channel_id = serializers.CharField()
    app_id = serializers.CharField()