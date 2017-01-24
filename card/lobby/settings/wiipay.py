# -*- coding:utf-8 -*-

from go.util import DotDict
from card.core.property.three import Property

WIIPAY = DotDict({
    'appid_wiipay_pay': '1508b05c057e3a676e1f93da6ade16e6',
    'appid_zx002_pay': 'e3a5ea398e9215655b3f2594949ade42',

    'app_conf':DotDict({
        '1508b05c057e3a676e1f93da6ade16e6':DotDict({
            "pubkey":"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgmFvs4mu2Yfx0as56xSP
aaEEiWl/VDQTEqhV8i9RoV6zeHGZFEOM3LolMZlH76F8nmK3dwERq22ClL+Vpj3P
NqZsbXHivKGtiK4+234Jvh6yCO4m8dan9VxNetqi0xcztelhosSHRBmBVs7DyzU3
Kmr8Hkvsz+mKJkqnCMv7n78ZnIJWEod4qVzQzCkzblj8jly96oiLb3/gj+gmxpw/
k8l1u3hZ3KZfFPf2DU/Mh5Vonpq8Za8KEDHw1JgbgEHzjCnpAVUiVKTREHHlS4s4
nETJMIrKCwRRCeuxVUw5zj11sSKT4VRsHhj0gJ5f5jWGwLGp8D1mMtllu2qu6uPW
GQIDAQAB
-----END PUBLIC KEY-----""",
            'notify_url':'http://120.27.103.99/three/wiipay/order/notify_zx001/',
            }),
        'e3a5ea398e9215655b3f2594949ade42':DotDict({
            "pubkey":"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgmFvs4mu2Yfx0as56xSP
aaEEiWl/VDQTEqhV8i9RoV6zeHGZFEOM3LolMZlH76F8nmK3dwERq22ClL+Vpj3P
NqZsbXHivKGtiK4+234Jvh6yCO4m8dan9VxNetqi0xcztelhosSHRBmBVs7DyzU3
Kmr8Hkvsz+mKJkqnCMv7n78ZnIJWEod4qVzQzCkzblj8jly96oiLb3/gj+gmxpw/
k8l1u3hZ3KZfFPf2DU/Mh5Vonpq8Za8KEDHw1JgbgEHzjCnpAVUiVKTREHHlS4s4
nETJMIrKCwRRCeuxVUw5zj11sSKT4VRsHhj0gJ5f5jWGwLGp8D1mMtllu2qu6uPW
GQIDAQAB
-----END PUBLIC KEY-----""",
            'notify_url':'http://120.27.103.99/three/wiipay/order/notify_zx002/',
            }),
        }),
    'wiipay_items':DotDict({
        Property.NEWBIE_COIN_BAG_ONE:DotDict({
            'pay_point_num':'0001',
            'order_desc':u"6元新手大礼包"
            }),
        Property.VIP_COIN_BAG:DotDict({
            'pay_point_num':'0002',
            'order_desc':u"30元VIP金币大礼包"
            }),
        Property.TWO_RMB_COINS:DotDict({
            'pay_point_num':'0003',
            'order_desc':u"2元金币包"
            }),       
        Property.SIX_RMB_COINS:DotDict({
            'pay_point_num':'0004',
            'order_desc':u"6元金币包"
            }),
        Property.QUICK_SIX_RMB_COINS:DotDict({
            'pay_point_num':'0005',
            'order_desc':u"快速6元购买"
            }),
        Property.QUICK_EIGHT_RMB_COINS:DotDict({
            'pay_point_num':'0006',
            'order_desc':u"快速8元购买"
            }),
        Property.THIRTY_RMB_COINS:DotDict({
            'pay_point_num':'0007',
            'order_desc':u"30元金币礼包"
            }),
        Property.FIFTH_RMB_COINS:DotDict({
            'pay_point_num':'0008',
            'order_desc':u"50元金币礼包"
            }),
        Property.HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':'0009',
            'order_desc':u"100元金币礼包"
            }),
        Property.THREE_HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':'0010',
            'order_desc':u"300元金币礼包"
            }),
        Property.THIRTY_RMB_COINS:DotDict({
            'pay_point_num':'0011',
            'order_desc':u"30元快速购买"
            }),
        Property.HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':'0012',
            'order_desc':u"100元快速购买"
            }),
        Property.NEWBIE_TWO_RMB_COINS:DotDict({
            'pay_point_num':'0013',
            'order_desc':u"2元新手礼包"
            }),
        Property.MONKEY_FIFTY_RMB_BAGS:DotDict({
            'pay_point_num':'0014',
            'order_desc':u"猴年大礼包"
            }),
        Property.EIGHT_HUNDRED_RMB_BAGS:DotDict({
            'pay_point_num':'0015',
            'order_desc':u"800元金币包"
            }),
        Property.LIMITED_GIFT_BAG:DotDict({
            'pay_point_num':'0016',
            'order_desc':u"6元限时礼包",
            }),
        Property.CAT_FOOD_GIFT_BAG:DotDict({
            'pay_point_num':'0017',
            'order_desc':u"猫粮礼包"
            }),
        Property.SUPER_BAG: DotDict({
            'pay_point_num': '0018',
            'order_desc': u"30元超值礼包",
        }),
        Property.VIP_BAG_NORMAL: DotDict({
            'pay_point_num': '0019',
            'order_desc': u"白银VIP礼包",
            }),
        Property.VIP_BAG_GOLD: DotDict({
            'pay_point_num': '0020',
            'order_desc': u"黄金VIP道具礼包",
            }),
        Property.VIP_BAG_DIAMOND: DotDict({
            'pay_point_num': '0021',
            'order_desc': u"蓝钻VIP道具礼包",
            }),
        Property.VIP_BAG_CROWN: DotDict({
            'pay_point_num': '0022',
            'order_desc': u"皇冠VIP道具礼包",
            }),
        })
})
