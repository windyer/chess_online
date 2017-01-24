# -*- coding:utf-8 -*-
import datetime
from go.util import DotDict
from card.core.enum import Vip
from card.core.property.three import Property
from card.core.charge import ITEMS

ACTIVITY = DotDict({
    'create_device_set':'Activity:Created:Device:Set',
    'updated_device_set':'Activity:Updated:Device:Set',
    'updated_player_key':'Activity:Updated:user_id:{0}',
    'comment_device_set':'Activity:comment_award:Device:Set',
    'comment_player_key':'Activity:comment_award:user_id:{0}',
    'charge_player_key':'Activity:charge_status:user_id:{0}',
    'activity_status_key':'Activity:activity_status',   
    'jackpot_currency_key':'Activity:jackpot_currency',
    'double_seventh': DotDict({
        'name': "七夕活动",
        'start_time': "20160809",
        'end_time': "20160816",
        'statistics_time': "20160809",
        'double_seventh_discount': 0,
        'double_seventh_logo': False,
    }),
    'activities':DotDict({
        1:DotDict({
            'name':'注册送金币',
            'start_time':datetime.datetime.today(),
            'end_time':datetime.datetime.today() + datetime.timedelta(days=3650),
            'platform':'all',
            'channel':'all',
            'version':'1.3',
            'module_path':'card.lobby.apps.activity.auto_award.register.CurrencyAward',
            'option':DotDict({
                'message':u"【恭喜】您首次登录游戏, 获得了{0}金币!",
                'reason':u"create_award",
                'award_currency':10000,
                }),
            }),
        2:DotDict({
            'name':'首充送金币',
            'start_time':datetime.datetime(2014, 4, 30, 18, 0, 0, 0),
            'end_time':datetime.datetime(2014, 5, 30, 18, 0, 0, 0),
            'platform':'all',
            'channel':'all',
            'version':'1.3',
            'module_path':'card.lobby.apps.activity.auto_award.charge.FirstChargeCurrencyAward',
            'option':DotDict({
                'reason':u"first_charge_award",
                'message':u"【恭喜】您首次充值金币包，获得了{0}金币奖励！",
                'award_currencys':DotDict({
                    Property.TWO_RMB_COINS : ITEMS.coins[Property.TWO_RMB_COINS].coin,
                    Property.SIX_RMB_COINS : ITEMS.coins[Property.SIX_RMB_COINS].coin,
                    Property.THIRTY_RMB_COINS : ITEMS.coins[Property.THIRTY_RMB_COINS].coin,
                    Property.TWENTY_RMB_COINS : ITEMS.coins[Property.TWENTY_RMB_COINS].coin,
                    Property.FIFTH_RMB_COINS : ITEMS.coins[Property.FIFTH_RMB_COINS].coin,
                    Property.HUNDRED_RMB_COINS : ITEMS.coins[Property.HUNDRED_RMB_COINS].coin,
                    Property.THREE_HUNDRED_RMB_COINS : ITEMS.coins[Property.THREE_HUNDRED_RMB_COINS].coin,
                    Property.NEWBIE_COIN_BAG_ONE : ITEMS.coins[Property.NEWBIE_COIN_BAG_ONE].coin,
                    Property.VIP_COIN_BAG : ITEMS.coins[Property.VIP_COIN_BAG].coin,
                    }),
                }),
            }),
        3:DotDict({
            'name':'每日免费小喇叭',
            'start_time':datetime.datetime.today(),
            'end_time':datetime.datetime.today() + datetime.timedelta(days=3650),
            'platform':'all',
            'channel':'all',
            'version':'1.1',
            'module_path':'card.lobby.apps.activity.auto_award.logon.FreeSpeakerAward',
            'option':DotDict({
                'message':u"你今日登录获得了{0}次免费小喇叭奖励! 成为VIP免费奖励更多! ",
                'vip_message':u"你是【{0}】, 今日登录获得了{1}次免费小喇叭奖励! ",
                }),
            }),
        4:DotDict({
            'name':'月度充值奖励',
            'start_time':datetime.datetime(2014, 4, 30, 18, 0, 0, 0),
            'end_time':datetime.datetime(2014, 5, 30, 18, 0, 0, 0),
            'platform':'all',
            'channel':'all',
            'version':'1.3',
            'daily_award':True,
            'module_path':'card.lobby.apps.activity.draw_award.monthly_charge.MonthlyChargeAward',
            'option':DotDict({
                'reason':u"monthly_charge_award",
                'message':u"【恭喜】您今日获得了充值返利奖励的{0}金币, 再充{1}元, 本月还可再多领取{2}金币哦~",
                'full_month_message':u"【恭喜】您今日获得了充值返利奖励的{0}金币！",
                'charge_criteria':30,
                'award_currency':DotDict({
                    30:DotDict({'currency':10000}),
                    60:DotDict({'currency':20000}),
                    100:DotDict({'currency':60000}),
                    200:DotDict({'currency':150000}),
                    1000:DotDict({'currency':800000}),
                    })
                }),
            }),
        5:DotDict({
            'name':'挑战排行榜',
            'start_time':datetime.datetime.today(),
            'end_time':datetime.datetime.today() + datetime.timedelta(days=3650),
            'platform':'all',
            'channel':'all',
            'version':'1.3',
            'daily_award':True,
            'module_path':'card.lobby.apps.activity.draw_award.rank_challenge.RankChallengeAward',
            'option':DotDict({
                'message':u"【恭喜】你昨日排名第{0},获得了{1}金币奖励！",
                'max_rank':3,
                'award_currency':DotDict({
                    1:1000000,
                    2:500000,
                    3:200000,
                    })
                }),
            }),
        6:DotDict({
            'name':'注册送小喇叭',
            'start_time':datetime.datetime.today(),
            'end_time':datetime.datetime.today() + datetime.timedelta(days=3650),
            'platform':'all',
            'channel':'all',
            'version':'1.1',
            'module_path':'card.lobby.apps.activity.auto_award.register.PropertyAward',
            'option':DotDict({
                'message':u"【恭喜】您首次登录游戏，获得了{0}个{1}奖励！",
                'item_id':Property.SPEAKER.item_id,
                'count':2,
                }),
            }),
        7:DotDict({
            'name':'更新送金币',
            'start_time':datetime.datetime(2014, 4, 30, 18, 0, 0, 0),
            'end_time':datetime.datetime(2014, 5, 30, 0, 0, 0, 0),
            'platform':'all',
            'channel':'all',
            'version':'1.1',
            'module_path':'card.lobby.apps.activity.auto_award.logon.UpdateAward',
            'option':DotDict({
                'reason':u"update_award",
                'message':u"【恭喜】你升级到{0}版本, 获得{1}金币奖励！",
                'vip_message':u"【恭喜】你是{0}, 升级到{1}版本获得{2}金币奖, 比普通玩家多获得{3}金币奖励！",
                'award_currency':DotDict({
                        Vip.NONE:50000,
                        Vip.NORMAL:250000, 
                        Vip.GOLD:350000,
                        Vip.DIAMOND:550000,
                        Vip.CROWN:1050000,
                        Vip.SUPREMACY:1050000,
                        }),
                }),
            }),
        8:DotDict({
            'name':'评论送金币',
            'start_time':datetime.datetime(2014, 4, 30, 18, 0, 0, 0),
            'end_time':datetime.datetime(2014, 5, 30, 0, 0, 0, 0),
            'platform':'all',
            'channel':'all',
            'version':'1.1',
            'module_path':'card.lobby.apps.activity.draw_award.comment_award.CommentAward',
            'option':DotDict({
                'message':u"【恭喜】你对游戏进行了五星好评价, 获得了{0}金币奖励！",
                'award_currency':50000,
                }),
            }),
        9:DotDict({
            'name':'豹子王大放送活动',
            'start_time':datetime.datetime(2015, 1, 1, 0, 0, 0, 0),
            'end_time':datetime.datetime(2016, 1, 1, 0, 0, 0, 0),
            'platform':'all',
            'channel':'all',
            'version':'1.1',
            'module_path':'card.lobby.apps.activity.auto_award.charge.ChargeCurrencyAward',
            'option':DotDict({
                'reason':u"activity_charge_award",
                'message':u"【恭喜】您获得豹子王大放送活动充值奖励{0}金币！",
                'award_currencys':DotDict({
                    Property.TWO_RMB_COINS : ITEMS.coins[Property.TWO_RMB_COINS].coin,
                    Property.SIX_RMB_COINS : ITEMS.coins[Property.SIX_RMB_COINS].coin,
                    Property.TWENTY_RMB_COINS : ITEMS.coins[Property.TWENTY_RMB_COINS].coin,
                    Property.THIRTY_RMB_COINS : ITEMS.coins[Property.THIRTY_RMB_COINS].coin,
                    Property.FIFTH_RMB_COINS : ITEMS.coins[Property.FIFTH_RMB_COINS].coin,
                    Property.HUNDRED_RMB_COINS : ITEMS.coins[Property.HUNDRED_RMB_COINS].coin,
                    Property.THREE_HUNDRED_RMB_COINS : ITEMS.coins[Property.THREE_HUNDRED_RMB_COINS].coin,
                    Property.NEWBIE_COIN_BAG_ONE : ITEMS.coins[Property.NEWBIE_COIN_BAG_ONE].coin,
                    Property.VIP_COIN_BAG : ITEMS.coins[Property.VIP_COIN_BAG].coin,
                    Property.QUICK_FOUR_RMB_COINS : ITEMS.quick_coins[Property.QUICK_FOUR_RMB_COINS].coin,
                    Property.QUICK_SIX_RMB_COINS : ITEMS.quick_coins[Property.QUICK_SIX_RMB_COINS].coin,
                    Property.QUICK_EIGHT_RMB_COINS : ITEMS.quick_coins[Property.QUICK_EIGHT_RMB_COINS].coin,
                    }),
                }),
            }),
        10:DotDict({
            'name':'测试期间小喇叭欢乐送',
            'start_time':datetime.datetime(2014, 4, 30, 18, 0, 0, 0),
            'end_time':datetime.datetime(2014, 5, 31, 0, 0, 0, 0),
            'platform':'all',
            'channel':'all',
            'version':'1.1',
            'module_path':'card.lobby.apps.activity.auto_award.logon.PropertyAward',
            'option':DotDict({
                'message':u"【恭喜】你在测试期间期间登录，获得了{0}个{1}奖励！",
                'item_id':Property.SPEAKER.item_id,
                'count':10,
                }),
            }),
        11:DotDict({
            'name':'测试期间购买打折',
            'start_time':datetime.datetime(2014, 4, 30, 18, 0, 0, 0),
            'end_time':datetime.datetime(2014, 9, 9, 0, 0, 0, 0),
            'platform':'all',
            'channel':'all',
            'version':'1.1',
            'module_path':'card.lobby.apps.activity.auto_award.purchase_discount.PurchaseDiscountAward',
            'option':DotDict({
                'reason':u"test_purchase_discount_award",
                'message':u"【恭喜】您获得测试期间购买XXX奖励享受{0}折优惠！",
                'discounts':DotDict({
                    Property.TURNER_TICKET : 0.8,
                    }),
                }),
            }),
        12:DotDict({
            'name':'娱乐场奖励增加50%',
            'start_time':datetime.datetime(2014, 9, 5, 18, 0, 0, 0),
            'end_time':datetime.datetime(2014, 9, 9, 0, 0, 0, 0),
            'platform':'all',
            'channel':'all',
            'version':'1.1',
            'module_path':'card.lobby.apps.activity.auto_award.amusement.TurnerCurrencyAward',
            'option':DotDict({
                'message':u"【恭喜】中秋期间翻牌游戏金币奖励，你多获得了{0}金币奖励！",
                'award_time':0.5,
                'reason':u"turner_activity",
                }),
            }),
        13:DotDict({
            'name':'慰问金',
            'start_time':datetime.datetime(2014, 9, 11, 18, 0, 0, 0),
            'end_time':datetime.datetime(2014, 9, 13, 0, 0, 0, 0),
            'platform':'all',
            'channel':'all',
            'version':'1.1',
            'module_path':'card.lobby.apps.activity.auto_award.logon.Compensate',
            'option':DotDict({
                'award_currency':50000,
                'reason':u"compensate",
                'message':u"【系统】由于运营商网络故障，游戏于9月11日出现间断不能访问，特向你发放5W慰问金！",
                }),
            }),
        14:DotDict({
            'name':'包月用户',
            'start_time':datetime.datetime.today(),
            'end_time':datetime.datetime.today() + datetime.timedelta(days=3650),
            'platform':'all',
            'channel':'all',
            'version':'1.1',
            'module_path':'card.lobby.apps.activity.auto_award.charge.MonthlyPlayerChargeAward',
            'option':DotDict({
                'reason':u"monthly_player_charge_award",
                'message':u"【恭喜】您是包月用户获得充值奖励{0}金币！",
                'award_currencys':DotDict({
                    Property.ONE_RMB_COINS : ITEMS.coins[Property.ONE_RMB_COINS].coin * 0.1,
                    Property.TWO_RMB_COINS : ITEMS.coins[Property.TWO_RMB_COINS].coin * 0.1,
                    Property.SIX_RMB_COINS : ITEMS.coins[Property.SIX_RMB_COINS].coin * 0.1,
                    Property.EIGHT_RMB_COINS : ITEMS.coins[Property.EIGHT_RMB_COINS].coin * 0.1,
                    Property.FIFTEEN_RMB_COINS : ITEMS.coins[Property.FIFTEEN_RMB_COINS].coin * 0.1,
                    Property.TWENTY_RMB_COINS : ITEMS.coins[Property.TWENTY_RMB_COINS].coin * 0.1,
                    Property.THIRTY_RMB_COINS : ITEMS.coins[Property.THIRTY_RMB_COINS].coin * 0.1,
                    Property.FIFTH_RMB_COINS : ITEMS.coins[Property.FIFTH_RMB_COINS].coin * 0.1,
                    Property.HUNDRED_RMB_COINS : ITEMS.coins[Property.HUNDRED_RMB_COINS].coin * 0.1,
                    Property.THREE_HUNDRED_RMB_COINS : ITEMS.coins[Property.THREE_HUNDRED_RMB_COINS].coin * 0.1,
                    Property.NEWBIE_COIN_BAG_ONE : ITEMS.coins[Property.NEWBIE_COIN_BAG_ONE].coin * 0.1,
                    Property.VIP_COIN_BAG : ITEMS.coins[Property.VIP_COIN_BAG].coin * 0.1,
                    }),
                }),
            }),
        15:DotDict({
            'name':'日充值奖励',
            'start_time':datetime.datetime.today(),
            'end_time':datetime.datetime.today() + datetime.timedelta(days=3650),
            'platform':'all',
            'channel':'all',
            'version':'1.7.0',
            'daily_award':True,
            'module_path':'card.lobby.apps.activity.draw_award.daily_charge_award.DailyChargeAward',
            'option':DotDict({
                'reason':u"daily_charge_award",
                'message':u"【恭喜】您{0}月{1}日充值{2}获得了充值返利奖励{3}金币~",
                'charge_criteria':30,
                'old_charge_criteria':6,
                'change_date':datetime.datetime(2016, 3, 22, 0, 0, 0, 0),
                'award_currency':DotDict({
                    30:DotDict({'currency':10000}),
                    100:DotDict({'currency':110000}),
                    300:DotDict({'currency':500000}),
                    800:DotDict({'currency':2000000}),
                    2000:DotDict({'currency':6660000}),
                    }),
                'old_currency':DotDict({
                    6:DotDict({'currency':20000}),
                    30:DotDict({'currency':130000}),
                    50:DotDict({'currency':250000}),
                    100:DotDict({'currency':580000}),
                    300:DotDict({'currency':2000000}),
                    })
                }),
            }),
        16:DotDict({
            'name':'豹子王大放送活动',
            'start_time':datetime.datetime(2016, 1, 4, 0, 0, 0, 0),
            'end_time':datetime.datetime(2016, 1, 4, 0, 0, 0, 0) + datetime.timedelta(days=3650),
            'platform':'all',
            'channel':'all',
            'version':'1.1',
            'module_path':'card.lobby.apps.activity.auto_award.charge.ChargeCurrencyAward',
            'option':DotDict({
                'reason':u"activity_charge_award",
                'message':u"【恭喜】您获得豹子王大放送活动充值奖励{0}金币！",
                'award_currencys':DotDict({
                    Property.TWO_RMB_COINS : ITEMS.coins[Property.TWO_RMB_COINS].coin,
                    Property.SIX_RMB_COINS : ITEMS.coins[Property.SIX_RMB_COINS].coin,
                    Property.TWENTY_RMB_COINS : ITEMS.coins[Property.TWENTY_RMB_COINS].coin,
                    Property.THIRTY_RMB_COINS : ITEMS.coins[Property.THIRTY_RMB_COINS].coin,
                    Property.FIFTH_RMB_COINS : ITEMS.coins[Property.FIFTH_RMB_COINS].coin,
                    Property.HUNDRED_RMB_COINS : ITEMS.coins[Property.HUNDRED_RMB_COINS].coin,
                    Property.THREE_HUNDRED_RMB_COINS : ITEMS.coins[Property.THREE_HUNDRED_RMB_COINS].coin,
                    Property.NEWBIE_COIN_BAG_ONE : ITEMS.coins[Property.NEWBIE_COIN_BAG_ONE].coin,
                    Property.VIP_COIN_BAG : ITEMS.coins[Property.VIP_COIN_BAG].coin,
                    Property.QUICK_FOUR_RMB_COINS : ITEMS.quick_coins[Property.QUICK_FOUR_RMB_COINS].coin,
                    Property.QUICK_SIX_RMB_COINS : ITEMS.quick_coins[Property.QUICK_SIX_RMB_COINS].coin,
                    Property.QUICK_EIGHT_RMB_COINS : ITEMS.quick_coins[Property.QUICK_EIGHT_RMB_COINS].coin,
                    Property.EIGHT_HUNDRED_RMB_BAGS : ITEMS.coins[Property.EIGHT_HUNDRED_RMB_BAGS].coin,
                    }),
                }),
            }),
        17:DotDict({
            'name':'春节棋牌3天乐',
            'start_time':datetime.datetime(2016, 2, 7, 0, 0, 0, 0),
            'end_time':datetime.datetime(2016, 2, 10, 0, 0, 0, 0),
            'platform':'all',
            'channel':'all',
            'version':'1.1',
            'module_path':'card.lobby.apps.activity.auto_award.charge.ChargeCurrencyAward',
            'option':DotDict({
                'reason':u"activity_charge_award",
                'message':u"【恭喜】您在欢乐春节,充值金币双倍回馈活动充值，获得了{0}金币奖励！",
                'award_currencys':DotDict({
                    Property.TWO_RMB_COINS : ITEMS.coins[Property.TWO_RMB_COINS].coin * 2,
                    Property.SIX_RMB_COINS : ITEMS.coins[Property.SIX_RMB_COINS].coin * 2,
                    Property.TWENTY_RMB_COINS : ITEMS.coins[Property.TWENTY_RMB_COINS].coin * 2,
                    Property.THIRTY_RMB_COINS : ITEMS.coins[Property.THIRTY_RMB_COINS].coin * 2,
                    Property.FIFTH_RMB_COINS : ITEMS.coins[Property.FIFTH_RMB_COINS].coin * 2,
                    Property.HUNDRED_RMB_COINS : ITEMS.coins[Property.HUNDRED_RMB_COINS].coin * 2,
                    Property.THREE_HUNDRED_RMB_COINS : ITEMS.coins[Property.THREE_HUNDRED_RMB_COINS].coin * 2,
                    Property.NEWBIE_COIN_BAG_ONE : ITEMS.coins[Property.NEWBIE_COIN_BAG_ONE].coin * 2,
                    Property.VIP_COIN_BAG : ITEMS.coins[Property.VIP_COIN_BAG].coin * 2,
                    Property.QUICK_FOUR_RMB_COINS : ITEMS.quick_coins[Property.QUICK_FOUR_RMB_COINS].coin * 2,
                    Property.QUICK_SIX_RMB_COINS : ITEMS.quick_coins[Property.QUICK_SIX_RMB_COINS].coin * 2,
                    Property.QUICK_EIGHT_RMB_COINS : ITEMS.quick_coins[Property.QUICK_EIGHT_RMB_COINS].coin * 2,
                    }),
                }),
            }),
        18:DotDict({
            'name':'充值奖池',
            'start_time':datetime.datetime.today(),
            'end_time':datetime.datetime.today() + datetime.timedelta(days=3650),
            'platform':'all',
            'channel':'all',
            'version':'1.6.0',
            'module_path':'card.lobby.apps.activity.auto_award.charge.JackpotChargeAward',
            'option':DotDict({
                'reason':u"activity_jackpot_award",
                'message':u"天赐祥福，您在充值奖池中斩获{0}金币！",
                'sample':10000000,
                'luck_award_base':10000,
                'award_record':1000000,
                'award_bulletin':10000000,
                'bulletin_duration':15,
                'bulletin_type':2,
                'bulletin_message':'恭喜{0}玩家在充值奖池中斩获{1}万金币奖励',
                'luck_infos':DotDict({
                    0.1:0.3, 0.2:0.3, 0.3:0.15, 0.4:0.05, 0.5:0.05, 0.6:0.05, 0.8:0.05, 1:0.05,
                    }),
                'award_infos':DotDict({
                    Property.TWO_RMB_COINS : DotDict({'pool':16000, 'probability':DotDict({
                        0.5:0, 0.1:0, 0.08:0, 0.06:0, 0.04:0, 0.02:0, 0.01:0, 0.005:0.00018, 0.001:0.0011}),
                        }),
                    Property.QUICK_TWO_RMB_COINS : DotDict({'pool':16000, 'probability':DotDict({
                        0.5:0, 0.1:0, 0.08:0, 0.06:0, 0.04:0, 0.02:0, 0.01:0, 0.005:0.00018, 0.001:0.0011}),
                        }),
                    Property.NEWBIE_COIN_BAG_ONE : DotDict({'pool':16000, 'probability':DotDict({
                        0.5:0, 0.1:0, 0.08:0, 0.06:0, 0.04:0, 0.02:0, 0.01:0, 0.005:0.00018, 0.001:0.0011}),
                        }),
                    Property.NEWBIE_TWO_RMB_COINS : DotDict({'pool':16000, 'probability':DotDict({
                        0.5:0, 0.1:0, 0.08:0, 0.06:0, 0.04:0, 0.02:0, 0.01:0, 0.005:0.00018, 0.001:0.0011}),
                        }),
                    Property.SIX_RMB_COINS : DotDict({'pool':48000, 'probability':DotDict({
                        0.5:0, 0.1:0, 0.08:0, 0.06:0, 0.04:0, 0.02:0, 0.01:0.0001, 0.005:0.00084, 0.001:0.0011}),
                        }),
                    Property.QUICK_SIX_RMB_COINS : DotDict({'pool':48000, 'probability':DotDict({
                        0.5:0, 0.1:0, 0.08:0, 0.06:0, 0.04:0, 0.02:0, 0.01:0.0001, 0.005:0.00084, 0.001:0.0011}),
                        }),
                    Property.NEWYEAR_SIX_RMB_BAGS : DotDict({'pool':48000, 'probability':DotDict({
                        0.5:0, 0.1:0, 0.08:0, 0.06:0, 0.04:0, 0.02:0, 0.01:0.0001, 0.005:0.00084, 0.001:0.0011}),
                        }),
                    Property.MONKEY_FIFTY_RMB_BAGS : DotDict({'pool':70400, 'probability':DotDict({
                        0.5:0, 0.1:0, 0.08:0, 0.06:0, 0.04:0, 0.02:0, 0.01:0.0002, 0.005:0.001, 0.001:0.0022}),
                        }),
                    Property.THIRTY_RMB_COINS : DotDict({'pool':240000, 'probability':DotDict({
                        0.5:0, 0.1:0, 0.08:0, 0.06:0, 0.04:0.0001, 0.02:0.0002, 0.01:0.0006, 0.005:0.0031, 0.001:0.0035}),
                        }),
                    Property.QUICK_THIRTY_RMB_COINS : DotDict({'pool':240000, 'probability':DotDict({
                        0.5:0, 0.1:0, 0.08:0, 0.06:0, 0.04:0.0001, 0.02:0.0002, 0.01:0.0006, 0.005:0.0031, 0.001:0.0035}),
                        }),
                    Property.FIFTH_RMB_COINS : DotDict({'pool':400000, 'probability':DotDict({
                        0.5:0, 0.1:0, 0.08:0, 0.06:0.0001, 0.04:0.0002, 0.02:0.0005, 0.01:0.001, 0.005:0.0032, 0.001:0.01}),
                        }),
                    Property.HUNDRED_RMB_COINS : DotDict({'pool':800000, 'probability':DotDict({
                        0.5:0, 0.1:0, 0.08:0.0001, 0.06:0.0002, 0.04:0.0005, 0.02:0.001, 0.01:0.003, 0.005:0.0058, 0.001:0.011}),
                        }),
                    Property.THREE_HUNDRED_RMB_COINS : DotDict({'pool':2400000, 'probability':DotDict({
                        0.5:0.00001, 0.1:0.0002, 0.08:0.0004, 0.06:0.0006, 0.04:0.001, 0.02:0.005, 0.01:0.01, 0.005:0.015, 0.001:0.012}),
                        }),
                    Property.EIGHT_HUNDRED_RMB_BAGS : DotDict({'pool':6400000, 'probability':DotDict({
                        0.5:0.00001, 0.1:0.001, 0.08:0.0015, 0.06:0.003, 0.04:0.005, 0.02:0.01, 0.01:0.02, 0.005:0.03, 0.001:0.04}),
                        }),
                    Property.VIP_BAG_NORMAL: DotDict({'pool':48000, 'probability':DotDict({
                        0.5:0, 0.1:0, 0.08:0, 0.06:0, 0.04:0, 0.02:0, 0.01:0.0001, 0.005:0.00084, 0.001:0.0011}),
                        }),
                    Property.VIP_BAG_GOLD: DotDict({'pool': 704000, 'probability': DotDict({
                        0.5: 0, 0.1: 0, 0.08: 0, 0.06: 0.000, 0.04: 0.0005, 0.02: 0.001, 0.01: 0.003,0.005: 0.005, 0.001: 0.01}),
                        }),
                    Property.VIP_BAG_DIAMOND: DotDict({'pool': 3104000, 'probability': DotDict({
                        0.5: 0.00001, 0.1: 0.0003, 0.08: 0.0006, 0.06: 0.001, 0.04: 0.002, 0.02: 0.005, 0.01: 0.01,
                        0.005: 0.015, 0.001: 0.012}),
                                                              }),
                    Property.VIP_BAG_CROWN: DotDict({'pool': 7104000, 'probability': DotDict({
                        0.5: 0.00001, 0.1: 0.001, 0.08: 0.002, 0.06: 0.004, 0.04: 0.006, 0.02: 0.01, 0.01: 0.02,
                        0.005: 0.03, 0.001: 0.04}),
                                                              }),
                    Property.SUPER_BAG: DotDict({'pool': 240000, 'probability': DotDict({
                        0.5: 0, 0.1: 0, 0.08: 0, 0.06: 0, 0.04: 0.0001, 0.02: 0.0002, 0.01: 0.0006,
                        0.005: 0.0031, 0.001: 0.0035}),
                                                              }),
                    }),
                }),
            }),

        }),


    'announcement':DotDict({
        'bull': DotDict({
            'title':u'游戏公告',
            'name': 'http://qmzbw.oss-cn-shanghai.aliyuncs.com/bzw_image/bull_title.png',
            'content': DotDict({
                'id':1,
                'power': 4,
                'image': '',
                'text': u"[fontColor=ff0000 fontSize=22]2.2版本更新-活动公告优化\n[/fontColor]"
                        u"[fontColor=000000 fontSize=18]1.全新活动公告系统，更多游戏活动第一时间知晓\n"
                        u"2.增加每日充值排行榜，每日最高可获得2亿金币。\n"
                        u"3.商城-特惠新增VIP金币大礼包。\n"
                        u"4.新增好友推荐功能，邀约好友玩游戏一掷千金乐翻天！\n"
                        u"5.修复部分bug，优化网络环境，更省流量！\n\n\n[/fontColor]"
                        u"[fontColor=ff0000 fontSize=22]防骗提示\n[/fontColor]"
                        u"[fontColor=000000 fontSize=18]        近期出现有人冒充客服QQ，向玩家索要游戏账号和密码，传言客服能帮助玩家将假邮箱更改为真邮箱账号！\n"
                        u"郑重申明：游戏账号一旦被绑定邮箱，不能进行更改！\n"
                        u"请认准客服唯一QQ3050858895，客服不会向玩家索要任何游戏账号和密码\n\n\n[/fontColor]"
                        u"[fontColor=ff0000 fontSize=22]严禁非法交易!\n[/fontColor]"
                        u"[fontColor=000000 fontSize=18]        我们是一款休闲娱乐的棋牌游戏，为提供良好的游戏环境，请广大玩家自觉抵制，对此官方郑重申明:\n"
                        u"1.禁止玩家在游戏内以卖币买币任何方式进行赌博行为，否则将做封号处理。\n"
                        u"2.对于利用不正当手段恶意获取金币的玩家，一经查实，将清除所有非法获得利益。\n\n\n[/fontColor]"
                        u"[fontColor=ff0000 fontSize=22]请玩家注意账号安全\n[/fontColor]"
                        u"[fontColor=000000 fontSize=18]        由于近期游戏内出现一些诈骗和非法盗取玩家金币的现象，不要将自己的游戏账号信息发给其他玩家。请妥善保管好自己的账号信息。\n[/fontColor]"
                        u"[fontColor=000000 fontSize=18]                    抵制不良游戏，拒绝盗版游戏\n"
                        u"                    注意自我保护，谨防上当受骗\n"
                        u"                    适度游戏益脑，沉迷游戏伤身\n"
                        u"                    合理安排时间，享受健康生活[/fontColor]",
                'event': '',
                'button': '',
                'option': None,
            }),
            'open_time': datetime.datetime(2016, 01, 01, 0, 0, 0, 0),
            'end_time': datetime.datetime(2027, 01, 01, 0, 0, 0, 0),
            'update_path': '',
            'channel': ['all'],
            'version': 'all',
        }),
        'diamond_player': DotDict({
            'title': u'钻石玩家招募',
            'name': 'http://qmzbw.oss-cn-shanghai.aliyuncs.com/bzw_image/diamond_player_tab_on.png',
            'content': DotDict({
                'id': 2,
                'power': 2,
                'image': 'http://qmzbw.oss-cn-shanghai.aliyuncs.com/bzw_image/diamond_player_board.png',
                'text': u'[fontColor=000000 fontSize=18]        为了答谢长期以来支持我们的玩家，现在推出钻石服务。只要达到对应条件的玩家即可申请专业的一对一钻石客服的服务，更有大量的专属活动供玩家参与。\n[/fontColor]'
                        u'[fontColor=ff0000 fontSize=18]【申请条件】从申请日开始，近30日一个游戏ID累计充值达到8888元\n[/fontColor]'
                        u'[fontColor=000000 fontSize=18]【申请流程】\n'
                        u'1.满足申请条件\n'
                        u'2.联系客服QQ：3050858895 申请钻石服务\n'
                        u'3.客服核实信息后提交审核（2个工作日）\n'
                        u'4.审核通过后钻石客服通过QQ与玩家联系，享受钻石服务\n'
                        u'【钻石福利】\n'
                        u'1.加入钻石奖励（8888万金币，每个玩家只能领取一次）\n'
                        u'2.每月专属活动\n'
                        u'3.每种专属活动\n'
                        u'4.各色丰富的游戏奖励\n'
                        u'5.新版本新玩法新功能优先体验\n'
                        u'6.更多特色福利\n[/fontColor]'
                        u'[fontColor=ff0000 fontSize=18]如果玩家出现以下行为则会被取消钻石服务\n[/fontColor]'
                        u'[fontColor=000000 fontSize=18]1.多账号重复申请钻石服务（每位玩家仅能申请一次）\n'
                        u'2.主动申请终止服务\n'
                        u'3.其他违规行为\n[/fontColor]',
                'event': '',
                'button': '',
                'option': None,
            }),
            'open_time': datetime.datetime(2016, 01, 01, 0, 0, 0, 0),
            'end_time': datetime.datetime(2027, 01, 01, 0, 0, 0, 0),
            'update_path': '',
            'channel': ['all'],
            'version': 'all',
        }),
        'onetoone': DotDict({
            'title':u'金币充值买一送一',
            'name': 'http://qmzbw.oss-cn-shanghai.aliyuncs.com/bzw_image/onetoone_title.png',
            'content': DotDict({
                'id': 3,
                'power': 3,
                'image': 'http://qmzbw.oss-cn-shanghai.aliyuncs.com/bzw_image/onetoone.png',
                'text': u'[fontColor=000000 fontSize=18]棋乐无穷，牌案惊奇\n'
                        u'百人激战众人乐，虎虎生威豹子王！\n'
                        u'即日起活动期间金币充值买一送一!\n'
                        u'时间: 2015年9月6日起\n[/fontColor]',
                'event': '',
                'button': '',
                'option': None,
            }),
            'open_time': datetime.datetime(2016, 01, 01, 0, 0, 0, 0),
            'end_time': datetime.datetime(2027, 01, 01, 0, 0, 0, 0),
            'update_path': '',
            'channel': ['all'],
            'version': 'all',
        }),
        'charge_rank': DotDict({
            'title': u'充值排行榜',
            'name': 'http://qmzbw.oss-cn-shanghai.aliyuncs.com/bzw_image/charge_rank_tab_on.png',
            'method':2,
            'content': DotDict({
                'id': 4,
                'no_charge_info': u'您还没有充值',
                'power': 1,
                'image': '',
                'text': u'',
                'event': 'rank',
                'button': '',
                'option': None,
                'rank':DotDict({
                }),
            }),
            'award_info_1': [u'每日累计充值金额x5万金币', u'每日累计充值金额x4万金币', u'每日累计充值金额x3万金币',
                      u'每日累计充值金额x2万金币', u'每日累计充值金额x1万金币'],
            'award_info_2': [u'2亿金币奖励', u'1亿金币奖励', u'8000万金币奖励',
                      u'5000万金币奖励', u'3000万金币奖励'],
            'method_award_1':[50000,40000,30000,20000,10000],
            'method_award_2':[200000000,100000000,80000000,50000000,30000000],
            'open_time': datetime.datetime(2016, 01, 01, 0, 0, 0, 0),
            'end_time': datetime.datetime(2027, 01, 01, 0, 0, 0, 0),
            'start_get_award':datetime.datetime(2016, 01, 01, 0, 0, 0, 0),
            'end_get_award': datetime.datetime(2027, 01, 01, 0, 0, 0, 0),
            'update_path': 'card.lobby.apps.activity.service.ChargeRankService',
            'channel': ['all'],
            'version': 'all',
            'rank_ratio':17,
            'urgent_event':u'【恭喜】{0}玩家在昨日充值排名中，获得{1}金币！',
        }),
        'invite': DotDict({
            'title': u'邀请奖励',
            'name': 'http://qmzbw.oss-cn-shanghai.aliyuncs.com/bzw_image/invite_reward_tab_on.png',
            'content': DotDict({
                'id': 5,
                'power': 0,
                'image': 'http://qmzbw.oss-cn-shanghai.aliyuncs.com/bzw_image/invite_reward_board.png',
                'text': u'[fontColor=000000 fontSize=18]        你的好友通过你发出的分享页面来到游戏，你将从该好友的每一笔充值中获得16%的一级奖励(不会从你好友的充值额度中扣除)。当你的好友通过分享页面带来他的好友，你将从他的好友的每一笔充值中获取8%的二级充值奖励[/fontColor]',
                'event': 'invite',
                'button': u'立即邀请',
                'option': None,
            }),
            'open_time': datetime.datetime(2016, 01, 01, 0, 0, 0, 0),
            'end_time': datetime.datetime(2027, 01, 01, 0, 0, 0, 0),
            'update_path': '',
            'channel': ['all'],
            'version': 'all',
        }),
    }),
})
