from rest_framework import serializers

class RankPlayer(serializers.Serializer):
    user_id    = serializers.IntegerField()
    nick_name  = serializers.CharField()
    avatar_url = serializers.CharField(read_only=True)

class CurrencyRank(RankPlayer):
    currency = serializers.IntegerField()

class GiftRank(RankPlayer):
    gift_count = serializers.IntegerField()
    gift_value = serializers.IntegerField()

class TodayIncomeMost(RankPlayer):
    today_income_most = serializers.IntegerField()
    round_max_win  = serializers.IntegerField()

class WeekFruitIncomeMost(RankPlayer):
    week_fruit_income_most = serializers.IntegerField()

class MonthlyRedEnvelopeSendMost(RankPlayer):
    monthly_red_envelope_send_most = serializers.IntegerField()

class ThreeChampionship(RankPlayer):
    three_win_currency = serializers.IntegerField()
    #three_award_currency = serializers.IntegerField()

class FruitChampionship(RankPlayer):
    fruit_win_currency = serializers.IntegerField()
    #fruit_award_currency = serializers.IntegerField()

class JackpotCurrency(RankPlayer):
    jackpot_currency = serializers.IntegerField()

class JackpotAward(RankPlayer):
    jackpot_award = serializers.IntegerField()
    jackpot_stamp = serializers.IntegerField()

class RankProfile(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    currency = serializers.IntegerField()
    nick_name = serializers.CharField(required=False)
    avatar_url = serializers.CharField(read_only=True)
    gift_value = serializers.IntegerField()
    gift_count = serializers.IntegerField()
    today_income_most = serializers.IntegerField()
    award_currency = serializers.IntegerField()
    round_max_win = serializers.IntegerField()
    week_fruit_income_most = serializers.IntegerField()
    monthly_red_envelope_send_most = serializers.IntegerField()
    three_win_currency = serializers.IntegerField()
    #three_award_currency = serializers.IntegerField()
    fruit_win_currency = serializers.IntegerField()
    #fruit_award_currency = serializers.IntegerField()
    jackpot_currency = serializers.IntegerField()
    jackpot_award = serializers.IntegerField()    
    jackpot_stamp = serializers.IntegerField()

class PersonalRanks(serializers.Serializer):
    currency = serializers.IntegerField()
    today_income_most = serializers.IntegerField()