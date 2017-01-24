# -*- coding:utf-8 -*-
from go.util import DotDict
from card.core.property.three import Property

class GiftCDType(object):
    FIVE_RMB_GIFT_BAG = 1
    TEN_RMB_GIFT_BAG = 2
    THREE_RMB_GIFT_BAG = 3
    SIX_RMB_GIFT_BAG = 4
    YOUKU_GIFT_BAG = 5


GIFTBAG = DotDict({
    'gift_cd_key':'Activity:GiftCDKey',
    'gift_cd_history':'Activity:GiftCDHistory',
    'gift_cd_stat':'Activity:GiftCDStat',
    'gift_content':DotDict({
        GiftCDType.FIVE_RMB_GIFT_BAG:(
            DotDict({'sub_item':Property.COIN, 'count':50000}),
            DotDict({'sub_item':Property.SOAP, 'count':1})),
        GiftCDType.TEN_RMB_GIFT_BAG:(
            DotDict({'sub_item':Property.COIN, 'count':120000}),
            DotDict({'sub_item':Property.SOAP, 'count':2}),
            DotDict({'sub_item':Property.BAD_EGG, 'count':2})),
        GiftCDType.THREE_RMB_GIFT_BAG:(
            DotDict({'sub_item':Property.COIN, 'count':40000}),),
        GiftCDType.SIX_RMB_GIFT_BAG:(
            DotDict({'sub_item':Property.COIN, 'count':60000}),),
        GiftCDType.YOUKU_GIFT_BAG:(
            DotDict({'sub_item':Property.COIN, 'count':120000}),
            DotDict({'sub_item':Property.SOAP, 'count':2}),
            DotDict({'sub_item':Property.BAD_EGG, 'count':2}),),
        })
        
})
