# -*- coding:utf-8 -*-

from go.util import DotDict
from card.core.enum import Vip
from card.core.property.three import Property

DAILY = DotDict({
    'login_awarded_device_set':'Daily:Logon:Device_id:Set',
    'awarded_player_set':'Daily:Logon:User_id:Set',
    'cat_award_criteria':1000000,
    'login_award':DotDict({
        'award_base':0,
        'max_days':5,
        'award_increment':2000,
        }),
    'online_awards':DotDict({
        1:66,
        2:666,
        3:866,
        4:1066,
        5:1166,
        6:1266,
        7:1366,
        8:1466,
        9:1566,
        10:1666,
        }),
    'monthly_payment_award':0,
    'rank_awards':DotDict({
        1:[DotDict({'item_id':Property.RABBIT_GIRL.item_id, 'count':1}),],
        2:[DotDict({'item_id':Property.SHIP.item_id, 'count':1}),],
        3:[DotDict({'item_id':Property.CAR.item_id, 'count':1}),],
        }),
    'messages':DotDict({
        'continous_login':u"【恭喜】您连续{0}天登录, 获得了{1}个{2}奖励!",
        'vip_award':u"【恭喜】您是【{0}】, 今日登录获得了{1}个{2}奖励!",
        'rank_ward':u"你在【昨日收入榜】排名第{0}, 获得了{1}个{2}奖励!",
        'monthly_payment_award':u"你是包月用户, 获得了{0}个{1}奖励!",
        'fortune_cat_award':u"【恭喜】您的招财猫今日为您吐了{0}金币, 多吃猫粮, 多吐金币哦~",
        }),
})