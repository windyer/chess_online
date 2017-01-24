# -*- coding:utf-8 -*-

from go.util import DotDict
from card.core.property.three import Property


YSDK = DotDict({
    'qq_app_id':"1105250083",
    'qq_app_key':'Rc0p4sC41gHN4b0b',
    'qq_login_url':'http://ysdk.qq.com/auth/qq_check_token', #normal server
    'wx_app_id':"wx9eca3f54528195e0",
    'wx_app_key':'41972d2c13cd80f3b52e674a264d6462',
    'wx_login_url':'http://ysdk.qq.com/auth/wx_check_token',#normal server
    'order_key':'rbZ30nMYztB04BznqX2siz14lp8jOB7f',
    'order_url':'https://ysdk.qq.com/mpay/pay_m',
    'url_path':'/v3/r/mpay/pay_m',
    'need_validate_form':True,
    'need_auth': True,
    'default_goods_url':'',
    'qq_session_id':'openid',
    'qq_session_type':'kp_actoken',
    'wx_session_id':'hy_gameid',
    'wx_session_type':'wc_actoken',
    'org_loc':'%2fmpay%2fpay_m',
    'ysdk_items':DotDict({
        Property.NEWYEAR_SIX_RMB_BAGS:DotDict({
            'pay_point_num':13052,
            'order_desc':u"6元新年礼包",
            'url':'',
            }),
        Property.VIP_COIN_BAG:DotDict({
            'pay_point_num':13053,
            'order_desc':u"30元VIP金币大礼包",
            'url':'',
            }),
        Property.TWO_RMB_COINS:DotDict({
            'pay_point_num':13054,
            'order_desc':u"2元金币包"
            }),
        Property.QUICK_FOUR_RMB_COINS:DotDict({
            'pay_point_num':13055,
            'order_desc':u"快速4元购买",
            'url':'',
            }),
        Property.SIX_RMB_COINS:DotDict({
            'pay_point_num':13056,
            'order_desc':u"6元金币包",
            'url':'',
            }),
        Property.QUICK_SIX_RMB_COINS:DotDict({
            'pay_point_num':13057,
            'order_desc':u"快速6元购买",
            'url':'',
            }),
        Property.QUICK_EIGHT_RMB_COINS:DotDict({
            'pay_point_num':13058,
            'order_desc':u"快速8元购买",
            'url':'',
            }),
        Property.THIRTY_RMB_COINS:DotDict({
            'pay_point_num':13059,
            'order_desc':u"30元金币礼包",
            'url':'',
            }),
        Property.FIFTH_RMB_COINS:DotDict({
            'pay_point_num':13060,
            'order_desc':u"50元金币礼包",
            'url':'',
            }),
        Property.HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':13061,
            'order_desc':u"100元金币礼包",
            'url':'',
            }),
        Property.THREE_HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':13062,
            'order_desc':u"300元金币礼包",
            'url':'',
            }),
        Property.THIRTY_RMB_COINS:DotDict({
            'pay_point_num':13063,
            'order_desc':u"30元快速购买",
            'url':'',
            }),
        Property.HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':13064,
            'order_desc':u"100元快速购买",
            'url':'',
            }),
        Property.ONE_RMB_COINS:DotDict({
            'pay_point_num':13065,
            'order_desc':u"1元新手金币包",
            'url':'',
            }),
        Property.NEWBIE_TWO_RMB_COINS:DotDict({
            'pay_point_num':13066,
            'order_desc':u"2元新手礼包",
            'url':'',
            }),
        Property.MONKEY_FIFTY_RMB_BAGS:DotDict({
            'pay_point_num':13067,
            'order_desc':u"猴年大礼包",
            'url':'',
            }),
        Property.EIGHT_HUNDRED_RMB_BAGS:DotDict({
            'pay_point_num':13068,
            'order_desc':u"800元金币包",
            'url':'',
            }),
        Property.NEWBIE_COIN_BAG_ONE:DotDict({
            'pay_point_num':13069,
            'order_desc':u"6元新手大礼包",
            'url':'',
            }),
        Property.LIMITED_GIFT_BAG:DotDict({
            'pay_point_num':13070,
            'order_desc':u"6元限时礼包",
            'url':'',
            }),
        Property.CAT_FOOD_GIFT_BAG:DotDict({
            'pay_point_num':21,
            'order_desc':u"猫粮礼包",
            }),
        Property.SUPER_BAG: DotDict({
            'pay_point_num': 22,
            'order_desc': u"30元超值礼包",
        }),
        Property.VIP_BAG_NORMAL: DotDict({
            'pay_point_num': 23,
            'order_desc': u"白银VIP礼包",
            }),
        Property.VIP_BAG_GOLD: DotDict({
            'pay_point_num': 24,
            'order_desc': u"黄金VIP道具礼包",
            }),
        Property.VIP_BAG_DIAMOND: DotDict({
            'pay_point_num': 25,
            'order_desc': u"蓝钻VIP道具礼包",
            }),
        Property.VIP_BAG_CROWN: DotDict({
            'pay_point_num': 26,
            'order_desc': u"皇冠VIP道具礼包",
            }),
        })
})
