# lobby server settings for development use
import traceback
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
    from appchina import *
    from coolpad import *
    from dianxin import *
    from luckbag import *
    from cat2currency import *
    from moguwan import *
    from ysdk import *
    from huawei import *
    from invite import *
except ImportError as ex:
    traceback.print_exc()

LOGGING.handlers.console.level = 'DEBUG'

SERVICE_REPOSITORYS = DotDict({
    'db':'card.api.db.service.service_repository', 
    'chat':'card.api.chat.service.service_repository',
})
HOLYTREE.api_view_available = True
