from rest_framework import serializers

class LotteryItem(serializers.Serializer):
    item_id = serializers.IntegerField()
    count = serializers.IntegerField()

class LotteryPhone(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13)
    item_id = serializers.IntegerField()
    count = serializers.IntegerField()

class LotteryQQ(serializers.Serializer):
    qq_number = serializers.CharField(max_length=10)
    item_id = serializers.IntegerField()
    count = serializers.IntegerField()