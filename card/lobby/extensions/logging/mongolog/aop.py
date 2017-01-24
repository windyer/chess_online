from datetime import datetime
import functools
from pymongo import errors
import redis
from go.containers.containers import Set

from card.core.conf import settings


def ignore_conn_error(func):
    @functools.wraps(func)
    def _(self, *args, **kwargs):
        try:
            ret = func(self, *args, **kwargs)
            return ret
        except (errors.AutoReconnect, errors.ConnectionFailure):
            self.logger.warn('conn lost to mongodb')
    return _


def realtime_currency_statistics(func):
    @functools.wraps(func)
    def _(self, *args, **kwargs):
        ret = func(self, *args, **kwargs)

        channel, delta = kwargs['channel'], kwargs['delta']
        timestamp = kwargs['timestamp']
        d = datetime.fromtimestamp(timestamp/1000.0).date().isoformat()

        _rdci_rdcw_update(func.func_name, channel, d, delta)
        _rdci_rdcw_update(func.func_name, 'holytree', d, delta)

        return ret
    return _


def realtime_charge_statistics(func):
    @functools.wraps(func)
    def _(self, *args, **kwargs):
        ret = func(self, *args, **kwargs)

        channel, price = kwargs['channel'], kwargs['price']
        user_id, timestamp = kwargs['user_id'], kwargs['timestamp']
        is_valid = kwargs.get('is_valid', True)
        d = datetime.fromtimestamp(timestamp/1000.0).date().isoformat()

        if is_valid == True:
            _rdcu_update(channel, user_id, d)
            _rdcu_update('holytree', user_id, d)
            _rdco_update(channel, d)
            _rdco_update('holytree', d)
            _rdcr_update(channel, d, price)
            _rdcr_update('holytree', d, price)

        return ret
    return _


def realtime_register_statistics(func):
    @functools.wraps(func)
    def _(self, *args, **kwargs):
        ret = func(self, *args, **kwargs)

        channel, timestamp = kwargs['channel'], kwargs['timestamp']
        d = datetime.fromtimestamp(timestamp/1000.0).date().isoformat()

        _rdnu_update(channel, d)
        _rdnu_update('holytree', d)# for all channel

        return ret
    return _


def realtime_login_statistics(func):
    @functools.wraps(func)
    def _(self, *args, **kwargs):
        ret = func(self, *args, **kwargs)

        user_id, channel = kwargs['user_id'], kwargs['channel']
        timestamp = kwargs['timestamp']
        d = datetime.fromtimestamp(timestamp/1000.0).date().isoformat()

        _rdau_update(channel, user_id, d)
        _rdau_update('holytree', user_id, d)# for all channel

        _rdat_update(channel, d)
        _rdat_update('holytree', d)# for all channel

        return ret
    return _


def _rdau_update(channel, user_id, d):
    key = 'rdau_'+ channel + '_' + d
    re = redis.Redis(**settings.PERSIST_REDIS)
    rdau_set = Set(key, re)
    rdau_set.sadd([user_id])


def _rdat_update(channel, d):
    key = 'rdat_'+ channel + '_' + d
    re = redis.Redis(**settings.PERSIST_REDIS)
    re.incr(key)


def _rdnu_update(channel, d):
    key = 'rdnu_'+ channel + '_' + d
    re = redis.Redis(**settings.PERSIST_REDIS)
    re.incr(key)


def _rdci_rdcw_update(scene, channel, d, delta):
    key = ''
    if scene == 'currency_issue':
        key = 'rdci_'
    elif scene == 'currency_withdrawal':
        key = 'rdcw_'

    key += channel + '_' + d
    re = redis.Redis(**settings.PERSIST_REDIS)
    re.incrby(key, delta)


def _rdcu_update(channel, user_id, d):
    key = 'rdcu_'+ channel + '_' + d
    re = redis.Redis(**settings.PERSIST_REDIS)
    rdcu_set = Set(key, re)
    rdcu_set.sadd([user_id])


def _rdco_update(channel, d):
    key = 'rdco_'+ channel + '_' + d
    re = redis.Redis(**settings.PERSIST_REDIS)
    re.incr(key)


def _rdcr_update(channel, d, price):
    key = 'rdcr_'+ channel + '_' + d
    re = redis.Redis(**settings.PERSIST_REDIS)
    re.incrby(key, price)