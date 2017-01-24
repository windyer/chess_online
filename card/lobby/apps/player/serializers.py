#coding=utf-8
import re

from rest_framework import serializers
from card.lobby.apps.store.serializers import PropertyItem
from card.lobby.apps.daily.serializers import DailyStatus
from card.lobby.apps.freebie.serializers import SalvageStatus, MoneyTreeStatus
from card.lobby.apps.activity.serializers import ActivityStatus
from card.lobby.apps.timeline.serializers import UreadEventCount
from card.lobby.apps.task.serializers import TaskInfo
from card.lobby.apps.rank.serializers import PersonalRanks, RankPlayer

alnum_reg = re.compile(r'^[a-zA-Z0-9]+$')
simple_reg = re.compile(r'^(([a-zA-Z0-9]))\1+$')
simple_group = ['123456', '1234567', '12345678', '123456789']

class DoubleSeventh(serializers.Serializer):
    male_id = serializers.IntegerField(required=False)
    male_name = serializers.CharField(required=False)
    female_id = serializers.IntegerField(required=False)
    female_name = serializers.CharField(required=False)

class LobbyNewbieItem(serializers.Serializer):
    item_id = serializers.IntegerField()
    price = serializers.IntegerField()
    coin = serializers.IntegerField()
    cat_food = serializers.IntegerField()

class OnlineConfigure(serializers.Serializer):
    customer_service = serializers.CharField(required=False)
    qq_group = serializers.CharField(required=False)
    enable_speaker = serializers.BooleanField(read_only=True)
    enable_game_chat = serializers.BooleanField(read_only=True)
    enable_three_chat = serializers.BooleanField(read_only=True)
    enable_turner = serializers.BooleanField(read_only=True)
    store_words = serializers.CharField(read_only=True)
    exclude_room_count = serializers.IntegerField(read_only=True)
    enable_game_online_award = serializers.BooleanField(read_only=True)
    enable_three_online_award = serializers.BooleanField(read_only=True)
    enable_daily_charge_award = serializers.BooleanField(read_only=True)
    enable_charge_double_award = serializers.BooleanField(read_only=True)
    activity_coin_multiple = serializers.IntegerField(read_only=True)
    enable_game_red_envelope = serializers.BooleanField(read_only=True)
    enable_three_red_envelope = serializers.BooleanField(read_only=True)
    enable_fruit_red_envelope = serializers.BooleanField(read_only=True)
    enable_monkey_fifty_money_bags = serializers.BooleanField(read_only=True)
    mall_money_bag_type = serializers.IntegerField(read_only=True)
    enable_gift_bag_exchange = serializers.BooleanField(read_only=True)
    enable_lottery_exchange = serializers.BooleanField(read_only=True)    
    enable_bull_download = serializers.BooleanField(read_only=True)    
    not_baidu_check_mode = serializers.BooleanField(read_only=True)
    startTime = serializers.IntegerField(read_only=True)
    endTime = serializers.IntegerField(read_only=True)
    all_chat = serializers.BooleanField(read_only=True)
    fruit_enabled = serializers.IntegerField(read_only=True)
    turncard_enabled= serializers.IntegerField(read_only=True)
    hundred_enabled = serializers.IntegerField(read_only=True)
    charge_limit = serializers.IntegerField(read_only=True)
    enable_activity = serializers.BooleanField(read_only=True)
    enable_luckbag = serializers.BooleanField(read_only=True)
    enable_cat2currency = serializers.BooleanField(read_only=True)
    enable_vip_treasure = serializers.BooleanField(read_only=True)
    enable_super_package = serializers.BooleanField(read_only=True)
    cat_cash_factor = serializers.IntegerField(read_only=True)
    cat_turn_weight = serializers.IntegerField(read_only=True)
    cat_min_weight = serializers.IntegerField(read_only=True)
    enable_invite = serializers.BooleanField(read_only=True)

class MonthStatistics(serializers.Serializer):
    charge_money = serializers.IntegerField()
    drawed_currency = serializers.IntegerField()

class NoChargeItems(serializers.Serializer):
    item_id = serializers.IntegerField()

class UpdateProfileRequest(serializers.Serializer):
    nick_name = serializers.CharField(required=False, min_length=1, max_length=100)
    gender = serializers.IntegerField(required=False, min_value=1, max_value=3)
    signature = serializers.CharField(required=False, max_length=100)
    contact = serializers.CharField(required=False, max_length=100)

class PlayerAlbum(serializers.Serializer):
    image_id = serializers.IntegerField()
    image_url = serializers.CharField()

class UpdateAlbumRequest(serializers.Serializer):
    image_id = serializers.IntegerField(min_value=0, max_value=7)
    image_url = serializers.CharField(min_length=1)

class DeleteAlbumRequest(serializers.Serializer):
    image_id = serializers.IntegerField(min_value=1, max_value=7)

class UpdateAvatarRequest(serializers.Serializer):
    image_id = serializers.IntegerField(min_value=1, max_value=7)

class BriefProfile(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    nick_name = serializers.CharField(required=False)
    gender = serializers.IntegerField(required=False)
    avatar_url = serializers.CharField(required=False)
    signature = serializers.CharField(required=False)
    contact = serializers.CharField(required=False)
    currency = serializers.IntegerField(read_only=True)
    cat_weight = serializers.IntegerField(read_only=True)
    total_rounds = serializers.IntegerField(read_only=True)
    total_win_rounds = serializers.IntegerField(read_only=True)
    total_lose_rounds = serializers.IntegerField(read_only=True)
    round_max_win = serializers.IntegerField(read_only=True)
    total_max_currency = serializers.IntegerField(read_only=True)
    max_hand_card = serializers.CharField(read_only=True)
    vip_title = serializers.IntegerField(read_only=True)
    is_gaming = serializers.BooleanField(read_only=True)
    property_items = PropertyItem(many=True, read_only=True)
    address = serializers.CharField(read_only=True)
    ranks = PersonalRanks(many=False, read_only=True)
    albums = PlayerAlbum(many=True, read_only=True)
    monthly_payment = serializers.BooleanField(read_only=True)

class LimitedItem(serializers.Serializer):
    item_id = serializers.IntegerField(read_only=True)
    end_time = serializers.IntegerField(read_only=True)

class LimitedItemBuy(serializers.Serializer):
    item_id = serializers.IntegerField(read_only=True)
    count = serializers.IntegerField(read_only=True)

class HighestAward(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    nick_name = serializers.CharField(read_only=True)
    currency = serializers.IntegerField(read_only=True)

class GameMinCash(serializers.Serializer):
    mode = serializers.IntegerField(read_only=True)
    level = serializers.IntegerField(read_only=True)
    min_cash = serializers.IntegerField(read_only=True)
    max_cash = serializers.IntegerField(read_only=True)
    capped_cash = serializers.IntegerField(read_only=True)

class FirstAward(serializers.Serializer):
    turner = HighestAward(required=False)
    three = HighestAward(required=False)
    fruit = HighestAward(required=False)

class DetailProfile(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    nick_name = serializers.CharField(required=False)
    gender = serializers.IntegerField(required=False)
    avatar_url = serializers.CharField(required=False, read_only=True)
    signature = serializers.CharField(required=False)
    contact = serializers.CharField(required=False)
    currency = serializers.IntegerField(read_only=True)
    cat_weight = serializers.IntegerField(read_only=True)
    max_cat_weight = serializers.IntegerField(read_only=True)
    bank_currency = serializers.IntegerField(read_only=True)
    total_rounds = serializers.IntegerField(read_only=True)
    total_win_rounds = serializers.IntegerField(read_only=True)
    total_lose_rounds = serializers.IntegerField(read_only=True)
    round_max_win = serializers.IntegerField(read_only=True)
    total_max_currency = serializers.IntegerField(read_only=True)
    max_hand_card = serializers.CharField(read_only=True)
    vip_title = serializers.IntegerField(read_only=True)
    is_gaming = serializers.BooleanField(read_only=True)
    is_threeing = serializers.BooleanField(read_only=True)
    is_fruiting = serializers.BooleanField(read_only=True)
    property_items = PropertyItem(many=True, read_only=True)
    continuous_login_days = serializers.IntegerField(read_only=True)
    token = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    ranks = PersonalRanks(many=False, read_only=True)
    daily_status = DailyStatus(many=False, read_only=True)
    month_statistic = MonthStatistics(many=False, read_only=True)
    charge_times = serializers.IntegerField(read_only=True)
    charge_money = serializers.IntegerField(read_only=True)
    activity_status = ActivityStatus(many=True, read_only=True)
    salvage_status = SalvageStatus(many=False, read_only=True)
    money_tree_status = MoneyTreeStatus(many=False, read_only=True)
    task_info = TaskInfo(many=False, read_only=True)
    yesterday_top_players = RankPlayer(many=True, read_only=True)
    yesterday_self_rank = serializers.IntegerField(read_only=True)
    no_charge_items = NoChargeItems(many=True, read_only=True)
    albums = PlayerAlbum(many=True, read_only=True)
    has_charged_coin = serializers.BooleanField(read_only=True)
    monthly_payment = serializers.BooleanField(read_only=True)
    first_day_login = serializers.BooleanField(read_only=True)
    monthly_payment_available = serializers.BooleanField(read_only=True)
    monthly_payment_end_time = serializers.IntegerField(read_only=True)
    is_identified = serializers.BooleanField(read_only=True)
    identify_image_url = serializers.CharField(read_only=True)
    online_configure = OnlineConfigure(many=False, read_only=True)
    next_online_award_step = serializers.IntegerField(read_only=True)
    identify_type = serializers.CharField(read_only=True)
    idiom_code = serializers.CharField(read_only=True)
    vip_award_step = serializers.IntegerField(read_only=True)
    created_days = serializers.IntegerField(read_only=True)
    newbie_item = LobbyNewbieItem()
    limited_item = LimitedItem(many=True, read_only=True)
    highest_award = FirstAward(read_only=True)
    game_min_cash = GameMinCash(many=True, read_only=True)
    bull_download_count = serializers.IntegerField(read_only=True)
    limited_item_buy_count = LimitedItemBuy(many=True, read_only=True)
    needUpdate = serializers.IntegerField(read_only=True)
    update_url = serializers.CharField(read_only=True)
    double_seventh_logo = serializers.BooleanField(read_only=True)
    double_seventh_discount = serializers.IntegerField(read_only=True)
    double_seventh = DoubleSeventh(many=False, read_only=True)


class UserList(serializers.Serializer):
    pass

class Refresh(serializers.Serializer):
    currency = serializers.IntegerField(read_only=True)
    bank_currency = serializers.IntegerField(read_only=True)
    cat_weight = serializers.IntegerField(read_only=True)
    vip_title = serializers.IntegerField(read_only=True)
    can_draw_task = serializers.BooleanField(read_only=True)
    ranks = PersonalRanks(many=False, read_only=True)
    concurrent_users = serializers.IntegerField(read_only=True)
    unread_events = UreadEventCount(many=False, read_only=True)
    enable_bull_download = serializers.BooleanField(read_only=True)
    enable_activity = serializers.BooleanField(read_only=True)
    double_seventh = DoubleSeventh(many=False, read_only=True)
    double_seventh_logo = serializers.BooleanField(read_only=True)
    double_seventh_discount = serializers.IntegerField(read_only=True)

class BankDetails(serializers.Serializer):
    currency = serializers.IntegerField(read_only=True)
    bank_currency = serializers.IntegerField(read_only=True)

class DepositRequest(serializers.Serializer):
    delta = serializers.IntegerField(required=True)
    auto_deposit = serializers.BooleanField(required=True)

class WithdrawRequest(serializers.Serializer):
    delta = serializers.IntegerField(required=True, min_value=1)
    password = serializers.CharField(required=True, min_length=1, max_length=50)

class BankPasswordRequset(serializers.Serializer):
    password = serializers.CharField(required=True, min_length=1, max_length=50)
    new_password = serializers.CharField(required=True, min_length=1, max_length=50)

class ForgetBankPasswordRequset(serializers.Serializer):
    pass


class ResetBankPasswordRequset(serializers.Serializer):

    new_password = serializers.CharField(min_length=6, max_length=16)
    confirm_password = serializers.CharField(min_length=6, max_length=16)

    def validate(self, attrs):
        new_password = attrs['new_password']
        confirm_password = attrs['confirm_password']

        if new_password != confirm_password:
            raise serializers.ValidationError(u"两次输入的密码不相同")
        if (simple_reg.match(new_password) or
                simple_reg.match(confirm_password) or
                new_password in simple_group or
                confirm_password in simple_group):
            raise serializers.ValidationError(u'密码设置过于简单')
        if not (alnum_reg.match(new_password) and alnum_reg.match(confirm_password)):
            raise serializers.ValidationError(u'输入错误')

        attrs['new_password'] = new_password
        attrs['confirm_password'] = confirm_password
        return attrs

class ReportRequest(serializers.Serializer):
    target_user_id = serializers.IntegerField()
    reason = serializers.CharField(max_length=50, required=False)
    context = serializers.CharField(max_length=500, required=False)

class IdentifyCodeRequest(serializers.Serializer):
    code = serializers.CharField(max_length=50, required=False)

class IdentifyCodeResponse(serializers.Serializer):
    is_identified = serializers.BooleanField(read_only=True)
    identify_image_url = serializers.CharField()

class IdentifyIdiomRequest(serializers.Serializer):
    code = serializers.CharField(max_length=50, required=False)

class IdentifyIdiomResponse(serializers.Serializer):
    is_identified = serializers.BooleanField(read_only=True)
    idiom_code = serializers.CharField(read_only=True)

class DrawVipBagRequest(serializers.Serializer):
    vip_title = serializers.IntegerField(max_value=4)

class DrawVipBagResponse(serializers.Serializer):
    bag_awards = PropertyItem(many=True, read_only=True)

class BeforeRequest(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
