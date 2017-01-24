# lobby server settings for test use

try:
    from common import *
    from django import *
    from logging import *
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
    from roulette import *
    from gift_bag import *
    from lottery import *
    from baidu import *
    from zhuoyi import *
    from bull_url import *
    from wiipay import *
    from youku import *
except ImportError as ex:
    import traceback
    traceback.print_exc()

LOGGING.handlers.console.level = 'DEBUG'
SERVICE_REPOSITORYS = DotDict({
    'db':'card.api.db.service.service_repository', 
    'chat':'card.api.chat.service.service_repository',
})
DEBUG = False
