# -*- coding:utf-8 -*-
from go.util import DotDict

REQUEST_FRIENDS_TRENDS_TYPE = 'request_friends'
MAKE_FRIENDS_TRENDS_TYPE = 'make_friends'
SEND_MESSAGE_TRENDS_TYPE = 'message'
SEND_CURRENCY_TRENDS_TYPE = 'send_currency'
SEND_GIFT_TRENDS_TYPE      = 'send_gift'

PENDING = 'pending'
ACCEPTED = 'accepted'
DECLINED = 'declined'

FRIEND = DotDict({
    'friend_count':20, 
    'supremacy_vip_friend_count':40,
    'cash_commission':0.20,
    'make_friend_currency_criterial':50000,
    'make_friend_win_rounds_criterial':5,
    'send_gift_currency_criterial':50000,
    'send_gift_win_rounds_criterial':1,
    'send_rose_msg' : "”{0}“送给”{1}“:999朵玫瑰花",
    'send_rabbit_msg' : "“{0}”送给“{1}”:兔女郎",
    'new_send_rose_msg' : "哇，好漂亮，”{0}“送给”{1}“:999朵玫瑰花",
    'new_send_rabbit_msg' : "“{0}”送给“{1}”:兔女郎,只要感情深，就送兔女郎",
    'max_nick_name' : 8,
})
