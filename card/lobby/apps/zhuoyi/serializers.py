from rest_framework import serializers

class ChargeNotifyRequest(serializers.Serializer):
    Recharge_Money = serializers.IntegerField()
    Extra = serializers.CharField(max_length=500)
    App_Id = serializers.IntegerField()
    Urecharge_Id = serializers.IntegerField()
    Uin = serializers.IntegerField()
    Create_Time = serializers.IntegerField()
    Recharge_Gold_Count = serializers.IntegerField()
    Recharge_Id = serializers.CharField()
    Sign = serializers.CharField()
    Pay_Status = serializers.IntegerField()

class ChargeNotifyRequestUUU(serializers.Serializer):
    Recharge_Money = serializers.CharField()
    Extra = serializers.CharField(max_length=500,required=False)
    App_Id = serializers.CharField()
    Urecharge_Id = serializers.CharField()
    Uin = serializers.CharField()
    Create_Time = serializers.CharField()
    Recharge_Gold_Count = serializers.CharField(required=False)
    Recharge_Id = serializers.CharField()
    Sign = serializers.CharField()
    Pay_Status = serializers.CharField()

class CreateOrderRequest(serializers.Serializer):
    item_id = serializers.IntegerField()
    channel_id = serializers.CharField()
    app_id = serializers.IntegerField()
