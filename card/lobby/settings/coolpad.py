# -*- coding:utf-8 -*-

from go.util import DotDict
from card.core.property.three import Property


COOLPAD = DotDict({
    "app_key": "f6ddc4af28d4428fbbbee8ae55fc7ead",
    "AppSecret": "807d6267a29493d0f982a212b41d9600",
    "PayKey": "bf54c29ad422fd847c92898a7103948a",
    'login_url': "https://openapi.coolyun.com/oauth2/token",
    'query_order_url': "http://pay.coolyun.com:6988/payapi/order",
    'app_id':"5000003342",
    'pubkey':'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDNelHDCn77Pa3hinm05aN3chZfRDFvVwyjozJV/DKHiSasSZvBg9AfZ6sjPQ3PAYZNfhm67HLtGeCb3o/dZR6TUjIHcdFYz/xG8MJJeEIEghYnEsYk3E3GsqV4ga6rRyUT8f2ymgtQlPVwknYIHAHLDbt2baShnnnarfiLpIfytwIDAQAB',
    'prvkey':'MIICXQIBAAKBgQCOX188DiGcEKbrmBgyEwb9hoySVmDXG0548WuUWvrmwnR4yj7vaNTsgmam63FrEEh9P63sxLJrHvDMdKnnyzcSAvCTFwTUphebskqgfH5Ooe1IwGdLsciHFyn9l8x3Vx6NLAJXDtUsXboA8nOw/VMG0KvtgaXMJIAXSjNh1prbUwIDAQABAoGAFjDpYCv3syKpUdlwFAYBNe0N5hVOnNilv5YppYMUznkKvHURoDFf1slwhJ34HK76DYOqcVgrUyUMdWHNxdJX79rhVgIlvcice7ucI35rTmCOGw4pHYM9ENhXc7CQ0wGET3Gc62StQoTWyOdOKgINU2arReri9Qm1J0bbmtnfQxkCQQDsfELLY8lGGH2xJXNrPljZfM7bfVl8GkN8KqqTeqHWKTqOeNv10L6E2Co+V1S5OkUOlVMFqHpTCuvNJhcLPt7tAkEAmh77rT+ojMYx01YrBgCcSv772tXBSAk77TDLVc5GBRkWBPSXmjdmDPoN4tK5CX7LbpFJzvH4Ad8A7y77UDsbPwJBAMDTuasaXH35blPJk8k4dz4vlIRIO3UD/U77g0bp0ZhM2eBeEAzp/s9Xa2qVzxGRv8laXO3aKJQZ7ZfDnTqgMykCQQCGv34F3DluUz5u6tCU3+XGQCdNDkR9ye0GFPpCXCWmAWfaD0uY/sSPpfSMEvbK0XvlgMuKTs4qPKJhfK8nV3YbAkBBB4Cw+uNQ0jXn5zOvc4j6HBfZ82ZQTswFq0GL/BTesUdFX2pwmFEb3otKWmKzpMDVT/aERaJ2xboA4KpgAa/U',
    "notify_url":"http://120.27.103.99/three/coolpay/charge-notify/",
    'need_validate_form':True,
    'need_auth': True,
    "channel": "zx022",
    'coolpad_items':DotDict({
        Property.NEWYEAR_SIX_RMB_BAGS:DotDict({
            'pay_point_num':11,
            'order_desc':u"6元新年礼包"
            }),
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
            'pay_point_num':7,
            'order_desc':u"100元快速购买"
            }),
        Property.ONE_RMB_COINS:DotDict({
            'pay_point_num':13065,
            'order_desc':u"1元新手金币包"
            }),
        Property.NEWBIE_TWO_RMB_COINS:DotDict({
            'pay_point_num':13,
            'order_desc':u"2元新手礼包"
            }),
        Property.MONKEY_FIFTY_RMB_BAGS:DotDict({
            'pay_point_num':13067,
            'order_desc':u"猴年大礼包"
            }),
        Property.EIGHT_HUNDRED_RMB_BAGS:DotDict({
            'pay_point_num':12,
            'order_desc':u"800元金币包"
            }),
        Property.NEWBIE_COIN_BAG_ONE:DotDict({
            'pay_point_num':13069,
            'order_desc':u"6元新手大礼包"
            }),
        Property.LIMITED_GIFT_BAG:DotDict({
            'pay_point_num':15,
            'order_desc':u"6元限时礼包"
            }),
        Property.CAT_FOOD_GIFT_BAG:DotDict({
            'pay_point_num':14,
            'order_desc':u"猫粮礼包"
            }),

        Property.SUPER_BAG: DotDict({
            'pay_point_num': 16,
            'order_desc': u"30元超值礼包",
        }),
        Property.VIP_BAG_NORMAL: DotDict({
            'pay_point_num': 17,
            'order_desc': u"白银VIP礼包",
            }),
        Property.VIP_BAG_GOLD: DotDict({
            'pay_point_num': 18,
            'order_desc': u"黄金VIP道具礼包",
            }),
        Property.VIP_BAG_DIAMOND: DotDict({
            'pay_point_num': 19,
            'order_desc': u"蓝钻VIP道具礼包",
            }),
        Property.VIP_BAG_CROWN: DotDict({
            'pay_point_num': 20,
            'order_desc': u"皇冠VIP道具礼包",
            }),
        })
})
