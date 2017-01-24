import time

from django.conf import settings

from go.containers import redis
from go.containers.containers import Hash

from card.core.util.key import Key
from card.core.util.timestamp import is_today

from card.lobby.apps.task.tasks import TaskManager

class StatusBase(type):

    def __init__(cls, name, bases, attrs):
        super(StatusBase, cls).__init__(name, bases, attrs)
        cls._key = Key(name)
        cls._redis = redis.Redis(**settings.PERSIST_REDIS)

class TaskStatus(object):

    __metaclass__ = StatusBase

    def award_status(self, user_id):
        status_hash = Hash(self._key[user_id], self._redis)
        award_status = status_hash.hgetall()
        tasks = TaskManager.tasks()
        status_dict = {}
        for task_id, task in tasks.iteritems():
            if str(task_id) in award_status:
                if not task.is_daily:
                    status_dict[task_id] = True
                else:
                    award_time = float(award_status[str(task_id)])
                    status_dict[task_id] = is_today(award_time)
            else:
                status_dict[task_id] = False
        return status_dict

    def has_awarded(self, user_id, task_id):
        status_dict = self.award_status(user_id)
        assert task_id in status_dict
        return bool(status_dict[task_id])

    def draw_award(self, user_id, task_id):
        assert task_id in TaskManager.tasks()
        status_hash = Hash(self._key[user_id], self._redis)
        status_hash.hset(task_id, time.time())
