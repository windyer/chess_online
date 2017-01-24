# -*- coding:utf-8 -*-

from go.util import DotDict
from card.core.property.three import Property

SKYPAY = DotDict({
    'secret_key':"sdsdg$^%&*(", 
    'merchant_id':"13984",
    'appid':"7010731",
    'appid_new':"7012431",
    'app_name':u"全民豹子王",
    'system_id':'300024',
    'notify_address':"http://120.27.103.99/three/skypay/order/notify/",
    'game_type':"1",
    'sms_limtation':DotDict({
        'active':False,
        "daily_device":60,
        "daily_user":30,
        "month_device":60,
        "month_user":30,
        }),
    'app_conf':DotDict({
        '7010731':DotDict({
            "appvkey": "MIICXAIBAAKBgQCrTjUffjxC55DvaVMhgAeL+RMFfqN6QHVNnW2AXmYYxSp+l13cSweyURtMFbl4JfTzGo6OW9UI05Hi0hJzMs8NvoifuEtxPvzUAC/ar80sKnKQNA4scCRdDf7Ttdu7heVh8sc5dKkh8ene1U+lcziIeLjZc5fpyhqbuh8OHQM3IwIDAQABAoGAU+HA24H5yh0P+FuPrFi/2UeGi+s965ACoJXU18XhooFxVHmUKVnIFAXpIvGEVxPnBN9dLNJE18SZrAKHrEcV4WszyphC5iS0VxohViqkLV5p0HKjmSaTM0inSh8eHs2XoNn9Cj9AaLE8cZ2PsfERl9u/bBN38e6AVNwhf4iAaMkCQQDunIODsxBn/xO/gDQ9hCRVc8aC9/Cp+JRStrBGGm/bLSvS+aHvGyIUlGC6660krj8I4O/oNFWXRLf+tTs8LqflAkEAt8oMdTMWS4MRxOQCysA+Vhc3KzYQjTfa23EWeFxTzEz1+1DTJlkiXoqbUu5lckIh9FYdY9JCzW8LDG+kUphiZwJAdripNv4BS70+timz1GfLLDlOrBtxQyDLq9v6GOdOgF8ZTv+l8rItYs/w0RAyNe38rw48T+y6KWmnorPJpUgRgQJBAKO881pa2EsQC32hMceWfDLQ3gq2UQqvL2F/n+g9QT7rdd6fxG4OzSrzS6wXzfN8bam0Ktzqzy8c9ffvYrNfJZMCQHL4ZR0azzxuTtapSnqY62CzooPzIj063aCZn8hLOxtj0CgTUkSCGrP+4mOLNkaNxVk9IqTukr3+kmFc0H4xKho=",
            "platpkey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+d2EivFCMepQfpJZhkaTCu5ipURBjZB3PQy/ijPHiUJcfRi8iEyktxptNWjmZJwPKvz7h/i7sm8jcmnvTwheWhjvTxQlTCqgbYbDLc642f5JhVnFqgF5wg4TE07D6iXO4e/4Pk9dnvOn9E/LWjERf9rDlaKf0ykPvlq+7AbB83QIDAQAB",
            'notify_url':"http://120.27.103.99/three/skypay/order/notify/",
            }),
        '7012431':DotDict({
            "appvkey": "MIICXAIBAAKBgQCbHcvd3qIaylCtuE1VL6JTAfeHM/vXj7GHXCxauk24vl4jOQ6mZurhHPlEGIj7Zc/QWPsahsYIEXpLTji/VOM/9u2Emih/6OXxg5yLEU3QRWRuhy5+nSW10C+5Zyc8NWGHOaHuq6owFDFgqY5AL7/exkB/NV78pEfNA3zfUPXpqwIDAQABAoGAYkuddvmwC/4M5ikWiFbpLGTgsMLWYqFiRH66dLv+qIWqLfPoPraVPRYZN3e8xmKcMFFSvlqNf2tj7fihqU1nu5JhLiP32d/qE+38XtctQpWrm/PggqHpzT5di6XHDVvnyIug9yuXzz9k4QC2aQ1VkBw8m3Pmgzssr9lBzzIB52ECQQDMYREi1yDxkOauz8N9E2xy5WXnQVuype7kjmQu/viFN+3lvdeuGCiJpXQz+ho4CW0BTxKep6ZPGAi4FNAWfPqDAkEAwktzyrhD23uIW+fJPwNoFQgXXECu3aZ036eItQPwFUX2wZepMKQfVwmfOWHvoB2GoViwZ4LDBa5WJxOhrdXLuQJAMPxi+xLNFplAcU3i8SuiprdNAWys6djTtXxbjtgWAPgy0Qn7lAK+VJ+PhpW/iwbXVaT6NYTBW9vK2zRB2+IAuQJBAKpqF5O07v+xaDaEJIV6bW4U/LhTm4yZlWUdwtBSNd/Sz82ZQjKBoWNr8xYXil+7xfv6mC8SCBARi0sW8vZP0TECQHQLKutx8kXSvbmXDJG5+0mmkiRHaLd4FHwIUgs9V+Gkzr7F/l3HprG3PVqoUw5gmJVQblf+ulXJiGsKtTPfPyQ=",
            "platpkey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCjUCc+qbMtJ5Z9E3n03oj9OR4wgHlA8Ko5uiOf7K8ch5np0fDwcreojwUgPSzOm9ISxeM1Er17tyeVte1qybN6+NyIRIHXTxcuWC6vw1RPmeVskwlBWv9Dkv5I7o4+GqJ3ARYrGeZ6GLHs/5zfX+z8f+VdcLSX8l1DYc1XEixGSQIDAQAB",
            "notify_url":"http://120.27.103.99/three/skypay/order/notify/",
            }),
    }),
    'skypay_items':DotDict({
        Property.NEWBIE_COIN_BAG_ONE:DotDict({
            'pay_point_num':1,
            'order_desc':u"仅需{0}元即可购买12万金币!"
            }),
        Property.VIP_COIN_BAG:DotDict({
            'pay_point_num':2,
            'order_desc':u"仅需{0}元即可购买60万金币!"
            }),
        Property.TWO_RMB_COINS:DotDict({
            'pay_point_num':3,
            'order_desc':u"仅需{0}元即可购买2万金币!"
            }),
        Property.QUICK_FOUR_RMB_COINS:DotDict({
            'pay_point_num':4,
            'order_desc':u"仅需{0}元即可购买4万金币!"
            }),
        Property.SIX_RMB_COINS:DotDict({
            'pay_point_num':5,
            'order_desc':u"仅需{0}元即可购买7万金币!"
            }),
        Property.QUICK_SIX_RMB_COINS:DotDict({
            'pay_point_num':5,
            'order_desc':u"仅需{0}元即可购买6万金币!"
            }),
        Property.QUICK_EIGHT_RMB_COINS:DotDict({
            'pay_point_num':6,
            'order_desc':u"仅需{0}元即可购买10万金币!"
            }),
        Property.THIRTY_RMB_COINS:DotDict({
            'pay_point_num':7,
            'order_desc':u"仅需{0}元即可购买40万金币!"
            }),
        Property.NEWBIE_PROPERTY_BAG_ONE:DotDict({
            'pay_point_num':8,
            'order_desc':u"新手道具特惠礼包（只能购买一次）, 仅需{0}元即可购买2个换牌卡+2个踢人卡+2个臭鸡蛋+2个防踢卡+2个肥皂!"
            }),
        Property.VIP_PROPERTY_BAG:DotDict({
            'pay_point_num':9,
            'order_desc':u"VIP道具大礼包(每级VIP每周可以购买一次), 仅需{0}元即可购买10个换牌卡+10个踢人卡+10个臭鸡蛋+10个防踢卡+10个肥皂!"
            }),
        Property.REPLACE_CARD_BAGS:DotDict({
            'pay_point_num':10,
            'order_desc':u"换牌卡道具包,仅需{0}元即可购买8个换牌卡!"
            }),
        Property.KICK_SEAT_CARD_BAGS:DotDict({
            'pay_point_num':11,
            'order_desc':u"踢人卡道具包,仅需{0}元即可购买8个踢人卡!"
            }),
        Property.AVOID_KICK_CARD_BAGS:DotDict({
            'pay_point_num':12,
            'order_desc':u"防踢卡道具包,仅需{0}元即可购买4个防踢卡!"
            }),
        Property.BAD_EGG_BAGS:DotDict({
            'pay_point_num':13,
            'order_desc':u"臭鸡蛋道具包,仅需{0}元即可购买8个臭鸡蛋!"
            }),
        Property.SOAP_BAGS:DotDict({
            'pay_point_num':14,
            'order_desc':u"肥皂包,仅需{0}元即可购买8个肥皂!"
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
        }),
    'pay_type':DotDict({
        'charge':'3',
        'property':'1',
        }),
    'check_items':DotDict({
        2:Property.TWO_RMB_COINS,
        4:Property.QUICK_FOUR_RMB_COINS,
        6:Property.SIX_RMB_COINS,
        8:Property.QUICK_EIGHT_RMB_COINS,
        30:Property.THIRTY_RMB_COINS,
        50:Property.FIFTH_RMB_COINS,
        100:Property.HUNDRED_RMB_COINS,
        300:Property.THREE_HUNDRED_RMB_COINS,
        }),
    'sms_items':[Property.NEWBIE_COIN_BAG_ONE, Property.TWO_RMB_COINS,
                Property.QUICK_FOUR_RMB_COINS, Property.SIX_RMB_COINS,
                Property.QUICK_SIX_RMB_COINS, Property.QUICK_EIGHT_RMB_COINS,
                Property.NEWBIE_PROPERTY_BAG_ONE, 
                Property.REPLACE_CARD_BAGS, Property.KICK_SEAT_CARD_BAGS,
                Property.AVOID_KICK_CARD_BAGS, Property.BAD_EGG_BAGS,
                Property.SOAP_BAGS,],
    'alipay_items':[Property.FIFTH_RMB_COINS, Property.HUNDRED_RMB_COINS,
                    Property.THREE_HUNDRED_RMB_COINS, Property.THIRTY_RMB_COINS,
                    Property.VIP_PROPERTY_BAG, Property.VIP_COIN_BAG,
                    Property.ONE_RMB_COINS,Property.NEWBIE_TWO_RMB_COINS, 
                    Property.NEWYEAR_SIX_RMB_BAGS,
                    Property.MONKEY_FIFTY_RMB_BAGS,
                    Property.EIGHT_HUNDRED_RMB_BAGS,
                    Property.LIMITED_GIFT_BAG,
                    Property.CAT_FOOD_GIFT_BAG,
                    Property.SUPER_BAG,
                    Property.VIP_BAG_NORMAL,
                    Property.VIP_BAG_GOLD,
                    Property.VIP_BAG_DIAMOND,
                    Property.VIP_BAG_CROWN,
                    ],
    "charge_types":DotDict({
        "test_123":DotDict({
            'sms_items':[],
            'alipay_items':[],
            }),
        }),
})