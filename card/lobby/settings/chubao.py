# -*- coding:utf-8 -*-

from go.util import DotDict
from card.core.property.three import Property


CHUBAO = DotDict({
    "app_key": "7168530813044808",
    "AppSecret": "0dbd2af4121f4aa095cc29f1ea82ae4d",
    "sellerid": "3215425917700589",
    "channel":"zx021",
    "notify_url":"http://120.27.103.99/three/chubao/charge-notify/",
    'need_validate_form':True,
    'need_auth': True,
    'tradeService':'com.zyxd.qmysz',
    'RSA_pubkey':"MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCd+7iQY/YMrikDUbShYxeJDyEBLglrci/eSV8USxW29BXBrB24sAKPuDqbF2YLyFS1XjAdz4YLYOqxpx05YgJz08Thl6rBVHFYzpQE7+LEf6xhG43WEhIf66QqhzB8sF1uN0kXCLkCkvt/M77nXjrqHjLQcjPJFKyX+Hz4RHiR2wIDAQAB",
    'RSA_prikey':"MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBALPghzN1LQbumVdeEiYbsw8BHhAzK2fafhAV0DAVeH3Le/CkEs//Z6cFHvWkD2dy/K7SjpNsb31TPptv1m8xKxqws65JKPHCaMSGCcMiQDutU0Tx/oVmjIzZj6CP1faC26163HOkVHXTHRMaE0lE+9W0CIjbLjAOsy8Z6j/wR7A7AgMBAAECgYBM8wxjkwkEIiYvHesdqlPbY1r9CybScsHjF7HMICM/jUEkHMx/dn9dD+/CncCJPMOj9idQId8/+dCapilRv/Lz7E/g1NPicgVr3J/lIl24f4Je2CayWOoWWH7IYTm3N47geDAM61bImYVeeFNSu89IoNQ9RhuW+b4/US0sK++owQJBAN7qyp9DdyYfjFRvVU3skbMX+9i/fI40q+kUmfZiROfe6JZ2+wU5ct97oocOZSGafnPMiDTUEKTIqPKbZEle4DMCQQDOkofMVRq3Y21IGsKLp1C8qWKkiVbKtzbbnWMnAGsjWcKZhDb0whMzyUBiD1iDWR5q9ciG3C0r2ZEnFZyjHMfZAkEA1nmSr/9KURzDeK2RpqK5YFXwEw/RuETHLj+LDrpnz6vxnmslg1ZNxuX+bvETrmwlxCaC2kk7JkCGBL4rlEg7bwJAe7Zzz6K0Qlowa3tjQaHtj19eLS33JaZ+Gx5x8Dym7V/nVGtDQmgsedowTcnk95zaw7H46xNXlihRbvfZfDJTWQJAAq4lIxlZFuM2Cr5PHiq/ZZqCUSIdYnHJWI/gX1g2SzjyfoeINm9UWZDTOornoO6+u33OogGPo6u6czr3NpqkTA==",
    'chubao_items':DotDict({
        Property.NEWYEAR_SIX_RMB_BAGS:DotDict({
            'pay_point_num':13052,
            'order_desc':u"6元新年礼包"
            }),
        Property.VIP_COIN_BAG:DotDict({
            'pay_point_num':13053,
            'order_desc':u"30元VIP金币大礼包"
            }),
        Property.TWO_RMB_COINS:DotDict({
            'pay_point_num':13054,
            'order_desc':u"2元金币包"
            }),
        Property.QUICK_FOUR_RMB_COINS:DotDict({
            'pay_point_num':13055,
            'order_desc':u"快速4元购买"
            }),
        Property.SIX_RMB_COINS:DotDict({
            'pay_point_num':13056,
            'order_desc':u"6元金币包"
            }),
        Property.QUICK_SIX_RMB_COINS:DotDict({
            'pay_point_num':13057,
            'order_desc':u"快速6元购买"
            }),
        Property.QUICK_EIGHT_RMB_COINS:DotDict({
            'pay_point_num':13058,
            'order_desc':u"快速8元购买"
            }),
        Property.THIRTY_RMB_COINS:DotDict({
            'pay_point_num':13059,
            'order_desc':u"30元金币礼包"
            }),
        Property.FIFTH_RMB_COINS:DotDict({
            'pay_point_num':13060,
            'order_desc':u"50元金币礼包"
            }),
        Property.HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':13061,
            'order_desc':u"100元金币礼包"
            }),
        Property.THREE_HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':13062,
            'order_desc':u"300元金币礼包"
            }),
        Property.THIRTY_RMB_COINS:DotDict({
            'pay_point_num':13063,
            'order_desc':u"30元快速购买"
            }),
        Property.HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':13064,
            'order_desc':u"100元快速购买"
            }),
        Property.ONE_RMB_COINS:DotDict({
            'pay_point_num':13065,
            'order_desc':u"1元新手金币包"
            }),
        Property.NEWBIE_TWO_RMB_COINS:DotDict({
            'pay_point_num':13066,
            'order_desc':u"2元新手礼包"
            }),
        Property.MONKEY_FIFTY_RMB_BAGS:DotDict({
            'pay_point_num':13067,
            'order_desc':u"猴年大礼包"
            }),
        Property.EIGHT_HUNDRED_RMB_BAGS:DotDict({
            'pay_point_num':13068,
            'order_desc':u"800元金币包"
            }),
        Property.NEWBIE_COIN_BAG_ONE:DotDict({
            'pay_point_num':13069,
            'order_desc':u"6元新手大礼包"
            }),
        Property.LIMITED_GIFT_BAG:DotDict({
            'pay_point_num':13070,
            'order_desc':u"6元限时礼包"
            }),
        Property.CAT_FOOD_GIFT_BAG:DotDict({
            'pay_point_num':13071,
            'order_desc':u"猫粮礼包"
            }),
        Property.SUPER_BAG: DotDict({
            'pay_point_num': 13072,
            'order_desc': u"30元超值礼包",
        }),
        Property.VIP_BAG_NORMAL: DotDict({
            'pay_point_num': 13073,
            'order_desc': u"白银VIP礼包",
            }),
        Property.VIP_BAG_GOLD: DotDict({
            'pay_point_num': 13074,
            'order_desc': u"黄金VIP道具礼包",
            }),
        Property.VIP_BAG_DIAMOND: DotDict({
            'pay_point_num': 13075,
            'order_desc': u"蓝钻VIP道具礼包",
            }),
        Property.VIP_BAG_CROWN: DotDict({
            'pay_point_num': 13076,
            'order_desc': u"皇冠VIP道具礼包",
            }),
        })
})
