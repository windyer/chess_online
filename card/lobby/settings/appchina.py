# -*- coding:utf-8 -*-

from go.util import DotDict
from card.core.property.three import Property


APPCHINA = DotDict({
    "app_id":"500176877",
    "app_key": "7168530813044808",
    "AppSecret": "0dbd2af4121f4aa095cc29f1ea82ae4d",
    "sellerid": "3215425917700589",
    "channel":"zx021",
    "notify_url":"http://120.27.103.99/three/appchina/charge_notify/",
    'need_validate_form':True,
    'need_auth': True,
    'tradeService':'com.zyxd.qmysz',
    'RSA_pubkey':"MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD2srC0ejyGRl6WadpyPIbjPeyDHDi4cTKn5QCqI245w3wQ8dwszrIE2Pppe9d8NKOsOSx/rsI7SaSyaeHzaM6kIws6NxVUW9wB53hGLkbHcFoUAD1+2nEjLJxjmmJ3MyDp0SIw0Uz9eExkB/ajNYBdJD+P+WCYM2M/OIRxYp4WIQIDAQAB",
    'RSA_prikey':"MIICWwIBAAKBgQCIpNslfS3++9oP1U+etRJHjEZ4vsLsiE0i25nVIYz988E/Ni+dR/Mu/XEOlJm3yO2Uococ60bfEgHOqB1LbBjn2kqmbFTaEMeZLgNOpIW42k1DSqgZQ5vnzLTyRe+DiOHD0ULiUTxX46igmBeHzkyr7wj42BgCvnQi+5jruY47/wIDAQABAoGAfBpONvRETCttV6gC0j/eREEw2AVZf/4jIJ+WTa5VIWi7gK+z+wMX6PuiLP3lxrekn7N5n15IVd1C6vBg+tlInCbb92Y0Lsufn9kbx0FxnjcmxBAY4+ObH5f8dmxTD8JF64b8D5SCsFq1MTNhDDPjcp5wMhuFvmdsZe+dAUFICFECQQDD0iY2hgWItSd8Aj5gLPfdmsdT0mZS7iy/dZ4lMAEkArce0D9kA+q32qsGAM2hC/tiy9oVevveaXeIV0nOs7FDAkEAsqMSAJ2mKOQBRA6IUWIj0+lb4COSWqqaYIn5TCfBRJTOy08XUxdSoNxQ7+q0aNSoHCCPQ+H/NLTTbn7ZI96wlQJAURiF1My6G/yR5oxzUpcs62x/IhqfX7bdd0j5foMb5dLuDWfG6N+qZAu+ChVpE0oICMlNftnY1yosY51qppzKSwJAXCIA4fJtRX+7K2e3ZQoR4nTkHukZzctZzdq7ikyiwIVjVraXGBLaWf7ne6X4oGy1u7QLT/6aiouM1Nt1kKuFNQJAaO1dA1SjV6AmoO0QfYPmYqdHLyETYZ0kIhKQHHF34rfRXeArHOpmCZJnODotcMIt8tATdKceMMg58rQ6osHoSA==",
    'appchina_items':DotDict({
        Property.NEWYEAR_SIX_RMB_BAGS:DotDict({
            'pay_point_num':1,
            'order_desc':u"6元新年礼包"
            }),
        Property.VIP_COIN_BAG:DotDict({
            'pay_point_num':2,
            'order_desc':u"30元VIP金币大礼包"
            }),
        Property.TWO_RMB_COINS:DotDict({
            'pay_point_num':3,
            'order_desc':u"2元金币包"
            }),
        Property.QUICK_FOUR_RMB_COINS:DotDict({
            'pay_point_num':4,
            'order_desc':u"快速4元购买"
            }),
        Property.SIX_RMB_COINS:DotDict({
            'pay_point_num':5,
            'order_desc':u"6元金币包"
            }),
        Property.QUICK_SIX_RMB_COINS:DotDict({
            'pay_point_num':6,
            'order_desc':u"快速6元购买"
            }),
        Property.QUICK_EIGHT_RMB_COINS:DotDict({
            'pay_point_num':7,
            'order_desc':u"快速8元购买"
            }),
        Property.THIRTY_RMB_COINS:DotDict({
            'pay_point_num':8,
            'order_desc':u"30元金币礼包"
            }),
        Property.FIFTH_RMB_COINS:DotDict({
            'pay_point_num':9,
            'order_desc':u"50元金币礼包"
            }),
        Property.HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':10,
            'order_desc':u"100元金币礼包"
            }),
        Property.THREE_HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':11,
            'order_desc':u"300元金币礼包"
            }),
        Property.THIRTY_RMB_COINS:DotDict({
            'pay_point_num':12,
            'order_desc':u"30元快速购买"
            }),
        Property.HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':13,
            'order_desc':u"100元快速购买"
            }),
        Property.ONE_RMB_COINS:DotDict({
            'pay_point_num':14,
            'order_desc':u"1元新手金币包"
            }),
        Property.NEWBIE_TWO_RMB_COINS:DotDict({
            'pay_point_num':15,
            'order_desc':u"2元新手礼包"
            }),
        Property.MONKEY_FIFTY_RMB_BAGS:DotDict({
            'pay_point_num':17,
            'order_desc':u"猴年大礼包"
            }),
        Property.EIGHT_HUNDRED_RMB_BAGS:DotDict({
            'pay_point_num':18,
            'order_desc':u"800元金币包"
            }),
        Property.NEWBIE_COIN_BAG_ONE:DotDict({
            'pay_point_num':16,
            'order_desc':u"6元新手大礼包"
            }),
        Property.LIMITED_GIFT_BAG:DotDict({
            'pay_point_num':19,
            'order_desc':u"6元限时礼包"
            }),
        Property.CAT_FOOD_GIFT_BAG:DotDict({
            'pay_point_num':20,
            'order_desc':u"猫粮礼包"
            }),
        Property.SUPER_BAG: DotDict({
            'pay_point_num': 21,
            'order_desc': u"30元超值礼包",
        }),
        Property.VIP_BAG_NORMAL: DotDict({
            'pay_point_num': 22,
            'order_desc': u"白银VIP礼包",
            }),
        Property.VIP_BAG_GOLD: DotDict({
            'pay_point_num': 23,
            'order_desc': u"黄金VIP道具礼包",
            }),
        Property.VIP_BAG_DIAMOND: DotDict({
            'pay_point_num': 24,
            'order_desc': u"蓝钻VIP道具礼包",
            }),
        Property.VIP_BAG_CROWN: DotDict({
            'pay_point_num': 25,
            'order_desc': u"皇冠VIP道具礼包",
            }),
        })
})
