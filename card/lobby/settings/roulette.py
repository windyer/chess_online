# coding=utf-8

from go.util import DotDict
from card.core.property.three import Property

ROULETTE = DotDict({
    'roulette_currency_criterial':100000,
    'roulette_items':(
        DotDict({'item':Property.ROULETTE_KICK_SEAT_CARDS, 'probability':0.02}),
        DotDict({'item':Property.ROULETTE_AVOID_KICK_CARDS, 'probability':0.17}),
        DotDict({'item':Property.ROULETTE_REPLACE_CARD, 'probability':0.1}),
        DotDict({'item':Property.ROULETTE_SOAP, 'probability':0.11}),
        DotDict({'item':Property.ROULETTE_COIN_1000, 'probability':0.09}),
        DotDict({'item':Property.ROULETTE_COIN_2000, 'probability':0.067}),
        DotDict({'item':Property.ROULETTE_BAD_EGG, 'probability':0.112}),
        DotDict({'item':Property.ROULETTE_LOTTERY_TICKET, 'probability':0.05}),
        DotDict({'item':Property.ROULETTE_CAT_FOOD, 'probability':0.001}),
        DotDict({'item':Property.ROULETTE_SOAP2, 'probability':0.11}),
        DotDict({'item':Property.ROULETTE_REPLACE_CARD2, 'probability':0.1}),
        DotDict({'item':Property.ROULETTE_BAD_EGG2, 'probability':0.12}),
        ), 
    'sample':10000000,
    'free_count':1,
    'record_key':"Roulette:Record:{0}",
    'roulette_history_key':"roulette_history",
    'roulette_details':DotDict({
        Property.ROULETTE_KICK_SEAT_CARDS: 
                DotDict({'sub_item':Property.KICK_SEAT_CARD, 'name':u"踢人卡"}),
        Property.ROULETTE_AVOID_KICK_CARDS: 
                DotDict({'sub_item':Property.AVOID_KICK_CARD, 'name':u"防踢卡"}),
        Property.ROULETTE_REPLACE_CARD: 
                DotDict({'sub_item':Property.REPLACE_CARD, 'name':u"换牌卡"}),
        Property.ROULETTE_SOAP: 
                DotDict({'sub_item':Property.SOAP, 'name':u"飞吻"}),
        Property.ROULETTE_COIN_1000: 
                DotDict({'sub_item':Property.COIN, 'count':1000, 'name':u"金币1000"}),
        Property.ROULETTE_COIN_2000: 
                DotDict({'sub_item':Property.COIN, 'count':2000, 'name':u"金币2000"}),
        Property.ROULETTE_BAD_EGG: 
                DotDict({'sub_item':Property.BAD_EGG, 'name':u"臭鸡蛋"}),
        Property.ROULETTE_LOTTERY_TICKET: 
                DotDict({'sub_item':Property.LOTTERY_TICKET, 'name':u"奖券"}),
        Property.ROULETTE_CAT_FOOD: 
                DotDict({'sub_item':Property.CAT_FOOD, 'name':u"猫粮"}),
        Property.ROULETTE_BAD_EGG2: 
                DotDict({'sub_item':Property.BAD_EGG, 'name':u"臭鸡蛋"}),
        Property.ROULETTE_REPLACE_CARD2: 
                DotDict({'sub_item':Property.REPLACE_CARD, 'name':u"换牌卡"}),
        Property.ROULETTE_SOAP2: 
                DotDict({'sub_item':Property.SOAP, 'name':u"飞吻"}),
    }),
    'currency_roulette_items':(
        DotDict({'item':Property.ROULETTE_KICK_SEAT_CARDS, 'probability':0.03}),
        DotDict({'item':Property.ROULETTE_AVOID_KICK_CARDS, 'probability':0.19}),
        DotDict({'item':Property.ROULETTE_REPLACE_CARD, 'probability':0.144}),
        DotDict({'item':Property.ROULETTE_SOAP, 'probability':0.15}),
        DotDict({'item':Property.ROULETTE_COIN_20000, 'probability':0.02}),
        DotDict({'item':Property.ROULETTE_COIN_50000, 'probability':0.01}),
        DotDict({'item':Property.ROULETTE_COIN_100000, 'probability':0.005}),
        DotDict({'item':Property.ROULETTE_BAD_EGG, 'probability':0.15}),
        DotDict({'item':Property.ROULETTE_LOTTERY_TICKET, 'probability':0.05}),
        DotDict({'item':Property.ROULETTE_CAT_FOOD, 'probability':0.001}),
        DotDict({'item':Property.ROULETTE_SOAP2, 'probability':0.15}),
        DotDict({'item':Property.ROULETTE_BAD_EGG2, 'probability':0.15}),
        ), 
    'currency_roulette_details':DotDict({
        Property.ROULETTE_KICK_SEAT_CARDS: 
                DotDict({'sub_item':Property.KICK_SEAT_CARD, 'name':u"踢人卡"}),
        Property.ROULETTE_AVOID_KICK_CARDS: 
                DotDict({'sub_item':Property.AVOID_KICK_CARD, 'name':u"防踢卡"}),
        Property.ROULETTE_REPLACE_CARD: 
                DotDict({'sub_item':Property.REPLACE_CARD, 'name':u"换牌卡"}),
        Property.ROULETTE_SOAP: 
                DotDict({'sub_item':Property.SOAP, 'name':u"飞吻"}),
        Property.ROULETTE_COIN_20000: 
                DotDict({'sub_item':Property.COIN, 'count':20000, 'name':u"金币20000"}),
        Property.ROULETTE_COIN_50000: 
                DotDict({'sub_item':Property.COIN, 'count':50000, 'name':u"金币50000"}),
        Property.ROULETTE_COIN_100000: 
                DotDict({'sub_item':Property.COIN, 'count':100000, 'name':u"金币100000"}),
        Property.ROULETTE_BAD_EGG: 
                DotDict({'sub_item':Property.BAD_EGG, 'name':u"臭鸡蛋"}),
        Property.ROULETTE_LOTTERY_TICKET: 
                DotDict({'sub_item':Property.LOTTERY_TICKET, 'name':u"奖券"}),
        Property.ROULETTE_CAT_FOOD: 
                DotDict({'sub_item':Property.CAT_FOOD, 'name':u"猫粮"}),
        Property.ROULETTE_BAD_EGG2: 
                DotDict({'sub_item':Property.BAD_EGG, 'name':u"臭鸡蛋"}),
        Property.ROULETTE_SOAP2: 
                DotDict({'sub_item':Property.SOAP, 'name':u"飞吻"}),
    }),
})