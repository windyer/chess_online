# coding=utf-8
from go.util import DotDict
from card.core.enum import Vip

TIME_LINE = DotDict({
    'max_count':50,
    'page_size':10,
    'max_unread':20,
    'trend_message_size':30,
    'friend_message_size':30,
    'personal_message_size':30,
    'personal_message_ttl':30*24*60*60,
    'system_message_size':10,
    'push_interval':DotDict({'gauss': (31104000, 10368000), 'min': 2592000}),
    'max_system_push':2,
    'personal_messages':DotDict({
        'register_greet':u"欢迎您登录游戏, 祝游戏愉快！",
        'task_award':u"【恭喜】您完成了'{0}'任务, 获得了{1}金币奖励！",
        'store_charge':u"【恭喜】您已成功购买【{0}】, 祝游戏愉快！",
        'monthly_charge':u"【恭喜】月度礼包今日获得了{0}金币, 祝游戏愉快！",
        'score_wall_award':u"【恭喜】您完成应用下载任务, 获得了{0}金币！",
        'monthly_complement':u"【恭喜】您购买了月度礼包, 本月本日前的{0}金币已经到帐!",
        }),
})