import time
import ujson
from datetime import datetime
from datetime import timedelta
import collections

from go.containers import redis
from go.containers.containers import (Hash, Set)
from django.conf import settings

from card.core.util.key import Key
from card.core.util.timestamp import is_today

class ContainersBase(type):

    def __init__(cls, name, bases, attrs):
        super(ContainersBase, cls).__init__(name, bases, attrs)
        cls._key = Key(name)
        cls._redis = redis.Redis(**settings.PERSIST_REDIS)


class SalvageStatus(object):

    __metaclass__ = ContainersBase

    def _update_salvage_status(self, user_id, status):
        salvage_hash = Hash(self._key, self._redis)
        salvage_hash.hset(user_id, ujson.dumps(status))

    def _salvaged_status(self, user_id):
        salvage_hash = Hash(self._key, self._redis)
        json_value = salvage_hash.hget(user_id)
        if json_value is not None:
            return collections.defaultdict(int, ujson.loads(json_value))
        else:
            return collections.defaultdict(int) 

    def get_salvage_info(self, user_id):
        salvaged_status = self._salvaged_status(user_id)
        last_salvaged_time = salvaged_status['time_stamp']
        if not is_today(last_salvaged_time):
            salvage_count = settings.FREEBIE.max_salvage_time
        else:
            salvage_count = settings.FREEBIE.max_salvage_time - salvaged_status['salvaged_count']

        resp = {}
        resp['salvage_interval'] = settings.FREEBIE.salvage_interval
        resp['max_salvage_count'] = settings.FREEBIE.max_salvage_time
        resp['salvage_currency'] = settings.FREEBIE.salvage_currency
        resp['salvage_criteria'] = settings.FREEBIE.salvage_currency_criteria
        resp['salvage_count'] = salvage_count if salvage_count > 0 else 0
        resp['next_salvage_time'] = int(last_salvaged_time) + settings.FREEBIE.salvage_interval - int(time.time())
        return resp

    def get_salvage_fund(self, user_id):
        salvaged_status = self._salvaged_status(user_id)
        last_salvaged_time = salvaged_status['time_stamp']
        if is_today(last_salvaged_time):
            salvaged_status['salvaged_count'] += 1;
        else:
            salvaged_status['salvaged_count'] = 1;
        salvaged_status['time_stamp'] = time.time()
        self._update_salvage_status(user_id, salvaged_status)

class MoneyTreeStatus(object):

    __metaclass__ = ContainersBase

    def _update_fetch_time(self, user_id, timestamp):
        money_tree_hash = Hash(self._key, self._redis)
        money_tree_hash.hset(user_id, timestamp)

    def _get_fetch_time(self, user_id):
        money_tree_hash = Hash(self._key, self._redis)
        str_value = money_tree_hash.hget(user_id)
        if str_value is not None:
            return int(str_value)
        else:
            return None

    def money_tree_status(self, user_id):
        now = datetime.now()

        noon_start_time = settings.FREEBIE.money_tree.noon_fetch_time[0]
        noon_end_time = settings.FREEBIE.money_tree.noon_fetch_time[1]
        today_noon_start_time = noon_start_time.replace(year=now.year, month=now.month, day=now.day)
        today_noon_end_time = noon_end_time.replace(year=now.year, month=now.month, day=now.day)

        evening_start_time = settings.FREEBIE.money_tree.evening_fetch_time[0]
        evening_end_time = settings.FREEBIE.money_tree.evening_fetch_time[1]
        today_evening_start_time = evening_start_time.replace(year=now.year, month=now.month, day=now.day)
        today_evening_end_time = evening_end_time.replace(year=now.year, month=now.month, day=now.day)

        fetch_time = self._get_fetch_time(user_id)
        fetch_date = None if fetch_time is None else datetime.fromtimestamp(fetch_time)
        
        if now < today_noon_start_time:
            fetch_end_date = today_noon_end_time
        elif now < today_noon_end_time:
            if fetch_date is None:
                fetch_end_date = today_noon_end_time
            elif fetch_date >= today_noon_start_time and fetch_date <= today_noon_end_time:
                fetch_end_date = today_evening_end_time
            else:
                fetch_end_date = today_noon_end_time
        elif now < today_evening_start_time:
            fetch_end_date = today_evening_end_time
        elif now < today_evening_end_time:
            if fetch_date is None:
                fetch_end_date = today_evening_end_time
            elif fetch_date >= today_evening_start_time and fetch_date <= today_evening_end_time:
                fetch_end_date = today_noon_end_time + timedelta(days=1)
            else:
                fetch_end_date = today_evening_end_time
        else:
            fetch_end_date = today_noon_end_time + timedelta(days=1)

        now_timestamp = int(time.time())
        fetch_end_timestamp = int(time.mktime(fetch_end_date.timetuple()))
        fetch_end_time = fetch_end_timestamp - now_timestamp
        
        resp = {}
        resp["can_fetch_now"] = fetch_end_time <= settings.FREEBIE.money_tree.fetch_interval_time
        resp['fetch_end_time'] = fetch_end_time
        resp['available_time'] = settings.FREEBIE.money_tree.available_time
        resp["fetch_interval_time"] = settings.FREEBIE.money_tree.fetch_interval_time

        return resp

    def get_money_tree_award(self, user_id):
        now = int(time.time())
        self._update_fetch_time(user_id, now)