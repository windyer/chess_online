import time
import ujson
from django.conf import settings

from go.containers import redis
from go.containers.containers import Hash

from card.core.util.key import Key
from card.core.property.three import Property
from card.core.util.timestamp import is_this_week, is_today
from django.utils import timezone
import datetime

current_timezone = timezone.get_current_timezone()

import card.lobby.apps.player.models as player_models
from card.core.util.timestamp import get_timestamp_for

class StatusBase(type):

    def __init__(cls, name, bases, attrs):
        super(StatusBase, cls).__init__(name, bases, attrs)
        cls._key = Key(name)
        cls._redis = redis.Redis(**settings.PERSIST_REDIS)


class ChargeStatus(object):

    __metaclass__ = StatusBase

    def charged_status(self, user_id):
        status_hash = Hash(self._key[user_id], self._redis)
        charge_status = status_hash.hgetall()

        status_dict = {}
        for item_id, item_status in charge_status.iteritems():
            item_id = int(item_id)
            if item_status is not None:
                item_status = ujson.loads(item_status)
            else:
                item_status = {}
                item_status['last_time_stamp'] = 0
                item_status["count"] = 0
            status_dict[item_id] = item_status

        return status_dict

    def item_charged_status(self, user_id, item_id):
        status_hash = Hash(self._key[user_id], self._redis)
        item_status = status_hash.hget(item_id)
        if item_status is not None:
            item_status = ujson.loads(item_status)
        else:
            item_status = {}
            item_status['last_time_stamp'] = 0
            item_status["count"] = 0
        return item_status

    def can_charge(self, user_id, vip_title, item_id):
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        package_type = player_extra.package_type
        if (package_type not in settings.STORE.newbie_charge_items and
            package_type not in settings.STORE.weekly_charge_items and
            package_type not in settings.STORE.daily_charge):
            return True

        weekly_items = settings.STORE.weekly_charge_items[package_type]
        newbie_items = settings.STORE.newbie_charge_items[package_type]
        daily_charge = settings.STORE.daily_charge[package_type]
        limited_items = settings.STORE.limited_charge_items[package_type]

        item_status = self.item_charged_status(user_id, item_id)
        if item_id in newbie_items:
            if item_status["count"] > 0:
                return False
        elif item_id in weekly_items:
            if is_this_week(item_status["last_time_stamp"]):
                return False
        elif item_id in daily_charge.daily_items:
            daily_counts = daily_charge.daily_counts
            if item_id not in daily_counts:
                return True
            if daily_counts[item_id][vip_title] <= 0:
                return False
            last_time_stamp = item_status["last_time_stamp"]
            charged_count = item_status["count"]
            if is_today(last_time_stamp) and charged_count >= daily_counts[item_id][vip_title]:
                return False

        if item_id in limited_items:
            life_time = limited_items[item_id]['life_time']
            today = timezone.now()
            created_time = player_extra.created_time.astimezone(current_timezone)
            delta = today - created_time
            seconds = delta.days * 24 * 3600 + delta.seconds
            if seconds >= life_time:
                return False

        return True

    def limited_item_end_time(self, user_id):
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        package_type = player_extra.package_type
        limited_items = settings.STORE.limited_charge_items[package_type]
        response = []       
        created_time = player_extra.created_time.astimezone(current_timezone)
        today = timezone.now()
        for item_id in limited_items:
            life_time = limited_items[item_id]['life_time']
            end_time = created_time + datetime.timedelta(seconds=life_time)
            if end_time <= today:
                continue
            response.append({'item_id':item_id.item_id, 'end_time':get_timestamp_for(end_time+datetime.timedelta(seconds=8*3600))})
        return response


    def no_charge_items(self, user_id, vip_title, package_type, channel):
        non_charge_items = []
        if package_type in settings.STORE.no_charge_items:
            non_charge_items = [{'item_id':item.item_id} for item in settings.STORE.no_charge_items[package_type]]
        if vip_title <= 0 and package_type in settings.STORE.weekly_charge_items:
            for item in settings.STORE.weekly_charge_items[package_type]:
                non_charge_items.append({'item_id':item.item_id})

        status_dict = self.charged_status(user_id)
        if package_type in settings.STORE.weekly_charge_items:
            weekly_items = settings.STORE.weekly_charge_items[package_type]
            for item in weekly_items:
                item_id = item.item_id
                if item_id not in status_dict:
                    continue
                status = status_dict[item_id]
                if is_this_week(status["last_time_stamp"]):
                    non_charge_items.append({'item_id':item_id})
        if package_type in settings.STORE.newbie_charge_items:
            newbie_items = settings.STORE.newbie_charge_items[package_type]
            for item in newbie_items:
                item_id = item.item_id
                if item_id not in status_dict:
                    continue
                status = status_dict[item_id]
                if status["count"] > 0:
                    non_charge_items.append({'item_id':item_id})
        if package_type in settings.STORE.daily_charge:
            daily_counts = settings.STORE.daily_charge[package_type].daily_counts
            daily_items = settings.STORE.daily_charge[package_type].daily_items
            for item in daily_items:
                item_id = item.item_id
                if item_id not in daily_counts:
                    continue
                if daily_counts[item_id][vip_title] <= 0:
                    non_charge_items.append({'item_id':item_id})
                    continue
                if item_id not in status_dict:
                    continue
                status = status_dict[item_id]
                if is_today(status["last_time_stamp"]) and status["count"] >= daily_counts[item_id][vip_title]:
                    non_charge_items.append({'item_id':item_id})

        return non_charge_items

    def charge(self, user_id, item_id):
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        package_type = player_extra.package_type

        if package_type in settings.STORE.weekly_charge_items:
            weekly_items = settings.STORE.weekly_charge_items[package_type]
        else:
            weekly_items = []
        if package_type in settings.STORE.newbie_charge_items:
            newbie_items = settings.STORE.newbie_charge_items[package_type]
        else:
            newbie_items = []
        if package_type in settings.STORE.weekly_charge_items:
            daily_items = settings.STORE.daily_charge[package_type].daily_items
        else:
            daily_items = []
        if not (item_id in weekly_items or item_id in newbie_items or item_id in daily_items):
            return

        item_status = self.item_charged_status(user_id, item_id)
        if item_id in weekly_items or item_id in newbie_items:
            item_status['last_time_stamp'] = int(time.time())
            item_status["count"] = 1
        elif item_id in daily_items:
            if is_today(item_status['last_time_stamp']):
                item_status["count"] += 1
            else:
                item_status["count"] = 1
            item_status['last_time_stamp'] = int(time.time())

        json_value = ujson.dumps(item_status)
        status_hash = Hash(self._key[user_id], self._redis)
        status_hash.hset(item_id, json_value)

        try:
            limited_items = settings.STORE.limited_charge_items[package_type]
            if item_id in limited_items:
                re = redis.Redis(**settings.PERSIST_REDIS)
                re.incr(settings.STORE.limited_item_count_key.format(item_id))
        except Exception as ex:
            print ex
            pass
    def get_limited_item_buy_count(self, user_id):
        re = redis.Redis(**settings.PERSIST_REDIS)
        response = []
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        package_type = player_extra.package_type
        limited_items = settings.STORE.limited_charge_items[package_type]
        package_type = player_extra.package_type
        for item_id in limited_items:
            cnt = re.get(settings.STORE.limited_item_count_key.format(item_id.item_id))
            count = 0
            if cnt is not None:
                count = int(int(cnt) * settings.STORE.limited_item_pro)
            response.append({'item_id':item_id.item_id, 'count':int(count)})
        return response

