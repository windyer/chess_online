from rest_framework import serializers

class DrawAwardRequest(serializers.Serializer):
    task_id = serializers.IntegerField()

class DrawAwardResponse(serializers.Serializer):
    currency = serializers.IntegerField()

class DailyStatistics(serializers.Serializer):
    total_rounds = serializers.IntegerField()
    win_ten_thousand_rounds = serializers.IntegerField()
    struggle_win_rounds = serializers.IntegerField()
    replaced_card_win_rounds = serializers.IntegerField()
    charge_money = serializers.IntegerField()
    turner_rounds = serializers.IntegerField()
    win_rounds = serializers.IntegerField()
    three_win_ten_thousand_rounds = serializers.IntegerField()
    
class NewBieStatistics(serializers.Serializer):
    total_rounds = serializers.IntegerField()
    receive_gift_count = serializers.IntegerField()
    send_gift_count = serializers.IntegerField()
    text_speaker_time = serializers.IntegerField()
    update_avatar_time = serializers.IntegerField()
    friend_count = serializers.IntegerField()
    win_rounds = serializers.IntegerField()
    integral_profile = serializers.IntegerField()
    bind_account = serializers.IntegerField()

class AwardedTask(serializers.Serializer):
    task_id = serializers.IntegerField()

class TaskInfo(serializers.Serializer):
    newbie = NewBieStatistics(many=False)
    daily = DailyStatistics(many=False)
    awarded_tasks = AwardedTask(many=True)