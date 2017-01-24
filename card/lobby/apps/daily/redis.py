import time
import ujson

from django.conf import settings

import go.containers
from go.containers import redis
from go.containers.containers import Hash

from card.core.util.key import Key
from card.core.util.timestamp import is_today

class StatusBase(type):

    def __init__(cls, name, bases, attrs):
        super(StatusBase, cls).__init__(name, bases, attrs)
        cls._key = Key(name)
        cls._redis = redis.Redis(**settings.PERSIST_REDIS)

class OnlineAwardStatus(object):

    __metaclass__ = StatusBase

    def award_status(self, user_id):
        status_hash = Hash(self._key, self._redis)
        status = status_hash.hget(user_id)
        if status == None:
            status = {"timestamp":0, "awarded_step":0}
        else:
            status = ujson.loads(status)
            if not is_today(status["timestamp"]):
                status = {"timestamp":0, "awarded_step":0}
        return status

    def next_award_step(self, user_id):
        status = self.award_status(user_id)
        step = status["awarded_step"] + 1
        return step

    def draw_award(self, user_id, award_step):
        assert award_step is not None
        status = self.award_status(user_id)
        status["awarded_step"] = award_step
        status["timestamp"] = int(time.time())
        status_hash = Hash(self._key, self._redis)
        status = status_hash.hset(user_id, ujson.dumps(status))    