
__all__ = ['dianxin_session_pool','appstore_session_pool', 'baidu_session_pool', 'iapppay_session_pool','youku_session_pool','yuyang_session_pool','chubao_session_pool','coolpad_session_pool','dianyou_session_pool','ysdk_session_pool']


from card.core.conf import settings
from card.core.util.pool import SessionPool, ServicePool

appstore_session_pool = SessionPool(
    'appstore', settings.POOL.appstore_size, settings.POOL.session_max_retries)
baidu_session_pool = SessionPool(
    'baidu', settings.POOL.baidu_size, settings.POOL.session_max_retries)
iapppay_session_pool = SessionPool(
    'iapppay', settings.POOL.iapppay_size, settings.POOL.session_max_retries)
youku_session_pool = SessionPool(
    'youku', settings.POOL.iapppay_size, settings.POOL.session_max_retries)
yuyang_session_pool = SessionPool(
    'yuyang', settings.POOL.iapppay_size, settings.POOL.session_max_retries)
chubao_session_pool = SessionPool(
    'chubao', settings.POOL.iapppay_size, settings.POOL.session_max_retries)
coolpad_session_pool = SessionPool(
    'coolpad', settings.POOL.iapppay_size, settings.POOL.session_max_retries)
dianyou_session_pool = SessionPool(
    'dianyou', settings.POOL.iapppay_size, settings.POOL.session_max_retries)
dianxin_session_pool = SessionPool(
    'dianxin', settings.POOL.iapppay_size, settings.POOL.session_max_retries)
ysdk_session_pool = SessionPool(
    'ysdk', settings.POOL.iapppay_size, settings.POOL.session_max_retries)