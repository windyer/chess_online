import time
import ujson
import datetime
from django.conf import settings
from django.utils import timezone

from go.containers import redis
from go.containers.containers import Hash

from card.core.util.key import Key
from card.core.util.timestamp import is_today
import card.lobby.apps.player.models as player_models


class StatusBase(type):

    def __init__(cls, name, bases, attrs):
        super(StatusBase, cls).__init__(name, bases, attrs)
        cls._key = Key(name)
        cls._redis = redis.Redis(**settings.PERSIST_REDIS)


class SkypayChargeStatus(object):

    __metaclass__ = StatusBase

    def _is_this_month(self, time_stamp):
        today = timezone.datetime.now()
        pay_date = datetime.datetime.fromtimestamp(time_stamp)
        return (pay_date.year == today.year and pay_date.month == today.month)

    def _update_sms_charge_status(self, status_hash, key, price):
        charge_status = status_hash.hget(key)
        if charge_status is None:
            charge_status = {}
            charge_status["last_time_stamp"] = 0
            charge_status["daily_sms_money"] = 0
        else:
            charge_status = ujson.loads(charge_status)

        if is_today(charge_status['last_time_stamp']):
            charge_status["daily_sms_money"] += price
        else:
            charge_status["daily_sms_money"] = price

        if self._is_this_month(charge_status['last_time_stamp']):
            charge_status["month_sms_money"] += price
        else:
            charge_status["month_sms_money"] = price

        charge_status["last_time_stamp"] = int(time.time())
        json_value = ujson.dumps(charge_status)
        status_hash.hset(item_id, json_value)


    def _sms_charge_status(self, status_hash, key):
        charge_status = status_hash.hget(key)
        if charge_status is None:
            charge_status = {}
            charge_status["last_time_stamp"] = 0
            charge_status["sms_money"] = 0
        else:
            charge_status = ujson.loads(charge_status)

        resp = {}
        if is_today(charge_status['last_time_stamp']):
            resp["daily_sms_money"] = charge_status["daily_sms_money"]
        else:
            resp["daily_sms_money"] = 0

        if self._is_this_month(charge_status['last_time_stamp']):
            resp["month_sms_money"] = charge_status["month_sms_money"]
        else:
            resp["month_sms_money"] = 0

        return resp

    def sms_status(self, user_id):
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        device_id = player_extra.login_device_id

        player_status_hash = Hash(self._key["user"], self._redis)
        device_status_hash = Hash(self._key["device"], self._redis)
        player_status = self._sms_charge_status(player_status_hash, user_id)
        device_status = self._sms_charge_status(device_status_hash, device_id)

        resp = {}
        resp["user"] = player_status
        resp["device"] = device_status
        return resp

    def charge(self, user_id, pay_method, item):
        if pay_method != "sms":
            return

        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        device_id = player_extra.login_device_id

        player_status_hash = Hash(self._key["user"], self._redis)
        device_status_hash = Hash(self._key["device"], self._redis)
        self._update_sms_charge_status(player_status_hash, user_id, item.price)
        self._update_sms_charge_status(device_status_hash, device_id, item.price)
