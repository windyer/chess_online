from rest_framework import serializers

from card.lobby.apps.store.serializers import PropertyItem

class DailyRequest(serializers.Serializer):
    pass

class DailyResponse(serializers.Serializer):
    currency = serializers.IntegerField(read_only=True)
    login_awards = PropertyItem(many=True, read_only=True)
    rank_awards = PropertyItem(many=True, read_only=True)
    vip_awards =  PropertyItem(many=True, read_only=True)
    monthly_payment_award = PropertyItem(many=True, read_only=True)
    fortune_cat_awards =  PropertyItem(many=True, read_only=True)

class DailyStatus(serializers.Serializer):
    daily_awarded = serializers.BooleanField()
    max_login_award = serializers.IntegerField(read_only=True)
    login_awards = PropertyItem(many=True, read_only=True)
    rank_awards = PropertyItem(many=True, read_only=True)
    vip_awards =  PropertyItem(many=True, read_only=True)
    monthly_payment_award = PropertyItem(many=True, read_only=True)
    fortune_cat_awards =  PropertyItem(many=True, read_only=True)

class OnlineAwardRequest(serializers.Serializer):
    pass

class OnlineAwardResponse(serializers.Serializer):
    next_award_step = serializers.IntegerField(read_only=True)
    award_currency = serializers.IntegerField(read_only=True)