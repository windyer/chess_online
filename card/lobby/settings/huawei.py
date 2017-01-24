# -*- coding:utf-8 -*-

from go.util import DotDict
from card.core.property.three import Property


HUAWEI = DotDict({
    'app_id':"10742938",
    "pay_id":"890086000102028915",
    'login_url':'https://api.vmall.com/rest.php',
    "notify_url":"http://120.27.103.99/three/dianyou/charge-notify/",
    "public_key":"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvubHtn4lWKye0GIxePjzHzSmrxo/AKUe/rUtF5XSiz+PXpSKO5SkUmv2gI2iG87uwzcrlYHGEv57LVakMf2zVDQles0aWsGDV/Rk44IdDb8Fmv+/YSHEu9EKbq4KJX/cuaL5mVv759ir++As675bo5Vyt5ANiziowZPwuE4G5j9/F9kMcE2z6WDA+uIvtZGba7R/gbD1vCSrTJsYjNZcVCs7j624SJ97kfrMQ89L6uaJJYbYN9b5l46FgijxQGVR3Vkud9DUDXtpLybJNRm+q+ARgbCRBLaGLKLuK/mOC/M+GRmw0+LliQs7AbINw6vvF+4jbz7QCJyhNkHENlxVtwIDAQAB",
    "private_key":"MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC+5se2fiVYrJ7QYjF4+PMfNKavGj8ApR7+tS0XldKLP49elIo7lKRSa/aAjaIbzu7DNyuVgcYS/nstVqQx/bNUNCV6zRpawYNX9GTjgh0NvwWa/79hIcS70Qpurgolf9y5ovmZW/vn2Kv74CzrvlujlXK3kA2LOKjBk/C4TgbmP38X2QxwTbPpYMD64i+1kZtrtH+BsPW8JKtMmxiM1lxUKzuPrbhIn3uR+sxDz0vq5oklhtg31vmXjoWCKPFAZVHdWS530NQNe2kvJsk1Gb6r4BGBsJEEtoYsou4r+Y4L8z4ZGbDT4uWJCzsBsg3Dq+8X7iNvPtAInKE2QcQ2XFW3AgMBAAECggEADllOXZsxt26SKVuYGF2t+IR+mt7AKY4/vClmEEXEo47NefB0S3Iqv785sgPzUV/GdonpDr3IY5kZLRk8Ej3dgtDAmHBeMMAm3S+Tfb5D7MqU40eh3O0q2msl+5e9T4BC2Pk1BZ/yWUTh+HarKbUPMkaDbuS2/+XsWVCDYXcL8bZm2dnPy+tmlvdRc3+ANEmvXL2K2AxXz/LtVTrWEpauDKLTvFn3/LpXigN3pn6s+v5Q6qlybjG+6QGgwxRTLQyS2I9TJFWhR/QLDzXSfbPdNhFyxCY9I0dp2e7IikVuqvtUn7wYxrOwQCKl0oeRBq89FtGF6YoQRvrsiGU2LQLvkQKBgQDjpWmtl/mw9Q6/RhZLIWWKe4YrQtwlYwbNBHJDCHpPAVtmckmEgjNWNcqEwwe8IeG4eE0/YfwT5EkGDiNKw3prhenl83CtSAFppQdfmQqNzbS/+5w0sUgVXBwDXZjhTiBDP3N8YaH003WG7abBtvPEydI+WQolJNlwfDGWSRwXowKBgQDWrb/WSLooCpFjKG4n8RlFgkVsy9BaDRlvrvIYRnopNukskdFR4YiB2MIfR+iJkO2+2jYcO2TEFtD+vahniKz1P++PAUTwiYoOVmtoLd3F0J96ZHSKZUe3hs1CRHP1X3LA5rU/1oesOR+8VQmNnyeZTuidhaD7E2hfo2r95Us63QKBgQCVIUbCrx2m3FMF4O831rADcXpqmslHQMEyy6fi3Anr+dKboWEiCn2BC4oZQP6vM28Afub0D8eobFOeQOLD1p07FSYuOzVkfxhV0gOrj8GHNewkHLuvFThIree4GLfPWXPvOgD4yajkjyad9s/YdXbqQuCVcZUg0iwT8Xg2oLxjiwKBgGFPkxTEFLYPzEVhT0WFsUnjuiqN3JzlMTGB4LWGRNuny1xroLF4BROuuJfLVan96vbHHR4BAjUsjoHaYJrFxnjJCYMONTy/a7gCDl/D4rJHVfL51CXjsPWNAj/WnaWNJYwxR9lvGkLEBhGtjk4G5cFFloXIy+bjrj0j61y5cjd1AoGAJyWfjPtx8KDcTET9BXNqCIUjNT/HZ3dwulTmD6w6WsxJsyiI0tdoR8T0j4qMx6yZyOVCq6x/ARiWpuOLV6ytckDHvRfMoqfKDYQOa+rSgdupbLVUvh0HE/vUMhewRvZoPsbknV9RyIhct44hKrTuZ37OE9EIekVs8IG0bWVp+w8=",
    'huawei_items':DotDict({
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
