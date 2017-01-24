# lobby server settings for production use
# coding=utf-8

try:
    from common import *
    from django import *
    from logging import *
    from mongo_logger import *
    from friend import *
    from rank import *
    from pool import *
    from timeline import *
    from store import *
    from coder_conversion import *
    from activity import *
    from game import *
    from update import *
    from freebie import *
    from daily import *
    from holytree import *
    from skypay import *
    from turner import *
    from player import *
    from vip import *
    from mobile import *
    from iapppay import *
    from roulette import *
    from gift_bag import *
    from lottery import *
    from baidu import *
    from zhuoyi import *
    from bull_url import *
    from wiipay import *
    from youku import *
    from dianyou import *
    from yuyang import *
    from chubao import *
    from coolpad import *
    from appchina import *
    from dianxin import *
    from luckbag import *
    from cat2currency import *
    from moguwan import *
    from ysdk import *
    from huawei import *
    from invite import *

except ImportError as ex:
    import traceback
    traceback.print_exc()
    raise ex

DEBUG = True 
LOGGING.handlers.console.level = 'DEBUG'
LOGGING.handlers.file.level = 'DEBUG'

SERVICE_REPOSITORYS = DotDict({
    'db':'card.api.db.service.service_repository', 
    'chat':'card.api.chat.service.service_repository',
})

DATA.port = 10089
CHAT_SERVER.host = '120.27.103.99'
CHAT_SERVER.port = 10010
CACHE_REDIS.port = 13379
PERSIST_REDIS.port = 13380

DATABASES['default']['USER'] = 'appfame'
DATABASES['default']['PASSWORD'] = 'three.appfame'
DATABASES['card.logger']['USER'] = 'appfame'
DATABASES['card.logger']['PASSWORD'] = 'three.appfame'

#DATABASES['default']['USER'] = 'qmbzw'
#DATABASES['default']['PASSWORD'] = 'holytreetech_com'
#DATABASES['default']['HOST'] = 'rdsrx104938j7d5676or.mysql.rds.aliyuncs.com'
#DATABASES['card.logger']['USER'] = 'qmbzw'
#DATABASES['card.logger']['PASSWORD'] = 'holytreetech_com'
#DATABASES['card.logger']['HOST'] = 'rdsrx104938j7d5676or.mysql.rds.aliyuncs.com'

CACHES['default']['LOCATION'] = '%s:%d' % (CACHE_REDIS.host, CACHE_REDIS.port)

SESSION_REDIS_HOST = CACHE_REDIS.host
SESSION_REDIS_PORT = CACHE_REDIS.port
SESSION_REDIS_DB = CACHE_REDIS.db

TIME_LINE.page_size = 20
TIME_LINE.max_unread = 15

RANK.expire_time = 60
RANK.max_size = 100

POOL.session_max_retries = 5

CODE_CONVERSION.need_encode = True

FRIEND.friend_count = 20
FRIEND.cash_commission = 0.20

GAME.concurrency_times = 6.2831852


TURNER.session_expire = 300
TURNER.profit_margin.low_criteria = 1.1
TURNER.profit_margin.high_criteria = 1.3
TURNER.probabilitys.player_win = [[0.6,0.61,0.27,0.1], [0.5,0.6,0.32,0.1], [0.5,0.6,0.3,0.1]]
TURNER.probabilitys.player_lose = [[0.6,0.5,0.27,0.07], [0.5,0.5,0.3,0.06], [0.5,0.6,0.3,0.07]]
TURNER.probabilitys.lucky_probs = [[0.6,0.6,0.27,0.1], [0.5,0.5,0.3,0.1], [0.5,0.5,0.3,0.1]]
