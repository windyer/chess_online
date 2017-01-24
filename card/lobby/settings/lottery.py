# coding=utf-8

from go.util import DotDict
from card.core.property.three import Property

LOTTERY = DotDict({
    'phone_number_len':13,
    'qq_number_len_min':5,
    'qq_number_len_max':11,
    'latest_count':10,
    'version':'1.7.0',
    'lottery_turner_enable':False,
    'lottery_charge_enable':False,
    'lottery_items':DotDict({
        Property.LOTTERY_ITEM_CAT_FOOD.item_id: DotDict({'name':'1袋猫粮', 'sub_item':Property.CAT_FOOD.item_id, 'count':1, 'consume':1000}),
        Property.LOTTERY_ITEM_COIN_10W.item_id: DotDict({'name':'100000金币', 'sub_item':Property.COIN.item_id, 'count':100000, 'consume':500}),
        Property.LOTTERY_ITEM_COIN_25W.item_id: DotDict({'name':'250000金币', 'sub_item':Property.COIN.item_id, 'count':250000, 'consume':1000}),
        Property.LOTTERY_ITEM_COIN_100W.item_id: DotDict({'name':'1000000金币', 'sub_item':Property.COIN.item_id, 'count':1000000, 'consume':3000}),
        }), 
    'phone_items':DotDict({
        Property.LOTTERY_PHONE_FEE_TEN.item_id: DotDict({'name':'10元话费卡', 'count':1, 'consume':1000}),
        Property.LOTTERY_PHONE_FEE_THIRTY.item_id: DotDict({'name':'30元话费卡', 'count':1, 'consume':3000}),
        Property.LOTTERY_PHONE_FEE_FIFTY.item_id: DotDict({'name':'50元话费卡', 'count':1, 'consume':5000}),
        }), 
    'qq_items':DotDict({
        Property.LOTTERY_QQ_FEE_TEN.item_id: DotDict({'name':'10Q币', 'count':1, 'consume':1000}),
        Property.LOTTERY_QQ_FEE_FIFTY.item_id: DotDict({'name':'50Q币', 'count':1, 'consume':5000}),
        }), 
})