# -*- coding:utf-8 -*-

from go.util import DotDict
from card.core.property.three import Property

ZHUOYI = DotDict({
    'app_id_kuku':"2551",
    'app_id_zx': "2882",
    'app_id_uuu':"3627",
    'app_conf':DotDict({
        '2551': DotDict({
            "app_key": "2a6a3d1f0c6622fb4d36cca50bc86c45",
            "secret_key": "ffa179ece6db6502e0d0dc358300247d",
            "notify_url": "http://120.27.103.99/three/zhuoyi/order/notify/",

            'channels': ('zy',),
        }),
        '2882': DotDict({
            "app_key": "43c0da39f5c0c023ded18bb6211431dc",
            "secret_key": "cbc6200e140a8f0d292c2cca6a9aadd9",
            "notify_url": "http://120.27.103.99/three/zhuoyi/order/notify_zx/",
            'channels': ('2882_01',),
        }),
        '3627': DotDict({
            "app_key": "wcTprJ6CTWwQ7uz1qYdTAweCnBdGQvkU",
            "secret_key": "a31826a9427bc02c95b36c3a77b0b1ca",
            "notify_url": "http://120.27.103.99/three/zhuoyi/order/notify_uuu/",
            'channels': ('3627_01',),
        }),

    }),
    'zhuoyi_items':DotDict({
        Property.VIP_COIN_BAG:DotDict({
            'pay_point_num':1,
            'order_desc':u"30元VIP金币大礼包"
            }),
        Property.TWO_RMB_COINS:DotDict({
            'pay_point_num':2,
            'order_desc':u"2元金币包"
            }),
        Property.SIX_RMB_COINS:DotDict({
            'pay_point_num':3,
            'order_desc':u"6元金币包"
            }),
        Property.QUICK_SIX_RMB_COINS:DotDict({
            'pay_point_num':4,
            'order_desc':u"快速6元购买"
            }),
        Property.QUICK_EIGHT_RMB_COINS:DotDict({
            'pay_point_num':5,
            'order_desc':u"快速8元购买"
            }),
        Property.THIRTY_RMB_COINS:DotDict({
            'pay_point_num':6,
            'order_desc':u"30元金币礼包"
            }),
        Property.HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':7,
            'order_desc':u"100元金币礼包"
            }),
        Property.THREE_HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':8,
            'order_desc':u"300元金币礼包"
            }),
        Property.THIRTY_RMB_COINS:DotDict({
            'pay_point_num':9,
            'order_desc':u"30元快速购买"
            }),
        Property.HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':10,
            'order_desc':u"100元快速购买"
            }),
        Property.NEWYEAR_SIX_RMB_BAGS:DotDict({
            'pay_point_num':11,
            'order_desc':u"6元新年礼包"
            }),
        Property.EIGHT_HUNDRED_RMB_BAGS:DotDict({
            'pay_point_num':12,
            'order_desc':u"800元金币包"
            }),
        Property.NEWBIE_TWO_RMB_COINS:DotDict({
            'pay_point_num':13,
            'order_desc':u"2元新手礼包"
            }),
        Property.CAT_FOOD_GIFT_BAG:DotDict({
            'pay_point_num':15,
            'order_desc':u"猫粮礼包",
            'url':'',
            }),
        Property.LIMITED_GIFT_BAG:DotDict({
            'pay_point_num':14,
            'order_desc':u"6元限时礼包"
            }),

        Property.SUPER_BAG: DotDict({
            'pay_point_num': 15,
            'order_desc': u"30元超值礼包",
        }),
        Property.VIP_BAG_NORMAL: DotDict({
            'pay_point_num': 16,
            'order_desc': u"白银VIP礼包",
            }),
        Property.VIP_BAG_GOLD: DotDict({
            'pay_point_num': 17,
            'order_desc': u"黄金VIP道具礼包",
            }),
        Property.VIP_BAG_DIAMOND: DotDict({
            'pay_point_num': 18,
            'order_desc': u"蓝钻VIP道具礼包",
            }),
        Property.VIP_BAG_CROWN: DotDict({
            'pay_point_num': 19,
            'order_desc': u"皇冠VIP道具礼包",
            }),
        })
})
