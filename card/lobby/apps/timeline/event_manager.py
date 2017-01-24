__all__ = ['FriendTrend', 'FriendMessage', 'PersonalMessage', 'TopSystemMessage', 'NormalSystemMessage']

import time
import ujson
from operator import itemgetter
import collections

import redis
from go.containers.containers import (Hash, List)
from django.conf import settings

from card.core.util.key import Key

class EventBase(type):

    def __init__(cls, name, bases, attrs):
        super(EventBase, cls).__init__(name, bases, attrs)
        cls._key = Key(name)
        cls._redis = redis.Redis(**settings.PERSIST_REDIS)


class EventList(object):

    __metaclass__ = EventBase

    PAGE_SIZE = settings.TIME_LINE.page_size
    MAX_EVENTS = settings.TIME_LINE.max_count

    def unread_count(self, user_id, key=None, share_list=False):
        key = key if key is not None else self._key
        list_key = key if share_list else key[user_id]
        max_unread_count = settings.TIME_LINE.max_unread
        event_list = List(list_key, db=self._redis)

        unread_count = 0
        last_fetch_time = self.fetch_time(user_id, key)
        for json_event in event_list.lrange(0, max_unread_count):
            event = ujson.loads(json_event)
            time_stamp = int(event['time_stamp'])

            if time_stamp > last_fetch_time:
                unread_count += 1
            else:
                break

        return unread_count

    def fetch_time(self, user_id, key=None):
        key = key if key is not None else self._key
        time_hash = Hash(key['fetch_time'], self._redis)

        fetch_time = time_hash.hget(user_id)
        return 0 if fetch_time is None else int(fetch_time)

    def update_fetch_time(self, user_id, key=None):
        key = key if key is not None else self._key
        time_hash = Hash(key['fetch_time'], self._redis)
        time_hash.hset(user_id, int(time.time()))

    def pages(self, total_count):
        pages = total_count // self.PAGE_SIZE
        pages = pages + 1 if total_count % self.PAGE_SIZE > 0 else pages
        return pages

    def get_events(self, user_id, page, key=None, share_list=False):
        key = key if key is not None else self._key
        list_key = key if share_list else key[user_id]
        event_list = List(list_key, db=self._redis)

        start = (page - 1) * self.PAGE_SIZE
        end = start + self.PAGE_SIZE - 1

        events = []
        event_list.ltrim(0, self.MAX_EVENTS)
        for json_event in event_list.lrange(start, end):
            event = ujson.loads(json_event)
            events.append(event)

        self.update_fetch_time(user_id, key)

        return self.pages(event_list.llen()), events

    def get_all_events(self, user_id, key=None, share_list=False):
        key = key if key is not None else self._key
        list_key = key if share_list else key[user_id]
        event_list = List(list_key, db=self._redis)
        
        events = []
        event_list.ltrim(0, self.MAX_EVENTS)
        for json_event in event_list.all():
            event = ujson.loads(json_event)
            events.append(event)

        self.update_fetch_time(user_id, key)

        return events

    def send_event(self, user_id, data, key=None, share_list=False):
        assert isinstance(data, dict)
        key = key if key is not None else self._key
        list_key = key if share_list else key[user_id]

        data['time_stamp'] = int(time.time())
        json_value = ujson.dumps(data)
        event_list = List(list_key, db=self._redis)
        event_list.lpush(json_value)

    def del_events(self, user_id, events, key=None, share_list=False):
        assert isinstance(events, (list, tuple))
        key = key if key is not None else self._key
        list_key = key if share_list else key[user_id]

        pipeline = self._redis.pipeline()
        event_list = List(list_key, pipeline=pipeline)
        for event in events:
            event_list.remove(event)
        pipeline.execute()


class FriendTrend(EventList):
    MAX_EVENTS = settings.TIME_LINE.trend_message_size

    def send_event(self, user_id, target_user_id, data):
        assert data['type'] != settings.SEND_MESSAGE_TRENDS_TYPE
        if data['type'] == settings.REQUEST_FRIENDS_TRENDS_TYPE:
            data['time_stamp'] = int(time.time())
            json_value = ujson.dumps(data)
            request_hash = Hash(self._key['request_friend'][target_user_id], self._redis)
            request_hash.hset(user_id, json_value)
        else:
            super(FriendTrend, self).send_event(target_user_id, data)

    def get_events(self, user_id, page):
        pages, events = super(FriendTrend, self).get_events(user_id, page)

        request_hash = Hash(self._key['request_friend'][user_id], self._redis)
        for json_event in request_hash.hvals():
            event = ujson.loads(json_event)
            events.append(event)
        events.sort(key=itemgetter('time_stamp'), reverse=True)

        return pages, events[0:self.PAGE_SIZE + 1]

    def del_request_event(self, user_id, target_user_id):
        request_hash = Hash(self._key['request_friend'][target_user_id], self._redis)
        request_hash.hdel(user_id)

class FriendMessage(EventList):
    MAX_EVENTS = settings.TIME_LINE.friend_message_size
    PAGE_SIZE = settings.TIME_LINE.page_size / 2

    def send_event(self, user_id, target_user_id, data):
        assert data['type'] == settings.SEND_MESSAGE_TRENDS_TYPE
        super(FriendMessage, self).send_event(target_user_id, data, self._key['inbox_list'][user_id])
        super(FriendMessage, self).send_event(user_id, data, self._key['outbox_list'][target_user_id])
        unread_hash = Hash(self._key['unread_count'][target_user_id], self._redis)
        unread_hash.hincrby(user_id, 1)

    def get_events(self, user_id, peer_user_id, page):
        out_pages, out_events = super(FriendMessage, self).get_events(user_id, page, self._key['outbox_list'][peer_user_id])
        in_pages, in_events = super(FriendMessage, self).get_events(user_id, page, self._key['inbox_list'][peer_user_id])

        messages = []
        messages.extend(out_events)
        messages.extend(in_events)
        messages.sort(key=itemgetter('time_stamp'), reverse=True)

        unread_hash = Hash(self._key['unread_count'][user_id], self._redis)
        unread_hash.hdel(peer_user_id)

        return (out_pages + in_pages), messages

    def del_friend_message(self, user_id, peer_user_id):
        outbox_list = List(self._key['outbox_list'][peer_user_id][user_id], db=self._redis)
        outbox_list.clear()
        inbox_list = List(self._key['inbox_list'][peer_user_id][user_id], db=self._redis)
        inbox_list.clear()
        unread_hash = Hash(self._key['unread_count'][user_id], self._redis)
        unread_hash.hdel(peer_user_id)

    def unread_message_info(self, user_id):
        unread_hash = Hash(self._key['unread_count'][user_id], self._redis)
        unread_infos = unread_hash.hgetall()

        return [{'user_id':int(k), 'count':int(v)} for k, v in unread_infos.iteritems()]


class PersonalMessage(EventList):
    MAX_EVENTS = settings.TIME_LINE.personal_message_size
    PAGE_SIZE = settings.TIME_LINE.page_size
    
    def reset_fetch_time(self, user_id):
        time_hash = Hash(self._key['fetch_time'], self._redis)
        time_hash.hset(user_id, 0)

    def reset_ttl_time(self, user_id):
        ttl = settings.TIME_LINE.personal_message_ttl
        personal_message_list = List(self._key[user_id], db=self._redis)
        personal_message_list.set_expire(ttl)

class SystemMessage(EventList):

    MAX_EVENTS = settings.TIME_LINE.system_message_size
    PAGE_SIZE = settings.TIME_LINE.page_size

    def unread_count(self, user_id):
        return super(SystemMessage, self).unread_count(user_id, share_list=True)

    def get_events(self, user_id):
        fetch_time = super(SystemMessage, self).fetch_time(user_id)
        messages = super(SystemMessage, self).get_all_events(user_id, share_list=True)

        resp = []
        for event in messages:
            if event['time_stamp'] > fetch_time:
                resp.append(event)
            else:
                break
        return resp

    def get_all_events(self, user_id):
        return super(SystemMessage, self).get_all_events(user_id, share_list=True)

    def send_message(self, message):
        super(SystemMessage, self).send_event(0, {'message':message}, share_list=True)

    def del_message(self, *messages):
        events = super(SystemMessage, self).get_all_events(0, share_list=True)
        deleting = [ujson.dumps(event) for message in messages for event in events
                    if event['message'] == message['message']]
        super(SystemMessage, self).del_events(0, deleting, share_list=True)

    def reset_fetch_time(self, user_id):
        time_hash = Hash(self._key['fetch_time'], self._redis)
        time_hash.hset(user_id, 0)

class TopSystemMessage(SystemMessage):
    pass

class NormalSystemMessage(SystemMessage):
    pass        

class SystemPush(EventList):

    __metaclass__ = EventBase

    def _last_push(self, device_id):
        fetch_hash = Hash(self._key[device_id], self._redis)

        time_stamp = fetch_hash.hget(device_id)
        return 0 if time_stamp is None else int(time_stamp)

    def _update_last_push(self, device_id, time_stamp):
        fetch_hash = Hash(self._key[device_id], self._redis)
        fetch_hash.hset(device_id, time_stamp)

    def get_all_push(self):
        event_list = List(self._key, db=self._redis)
        events = [ujson.loads(event) for event in event_list.lrange(0, -1)]
        return events

    def get_push(self, device_id):
        event_list = List(self._key, db=self._redis)
        last_push_time = self._last_push(device_id)
        events = []
        newest_push_time = 0

        event_list.ltrim(0, settings.TIME_LINE.max_system_push)
        for json_event in event_list.lrange(0, -1):
            event = ujson.loads(json_event)
            start_time = int(event['start_time'])
            end_time = int(event['end_time'])
            time_stamp = int(event['time_stamp'])

            now = int(time.time())
            if now < start_time or now > end_time:
                break 
            if last_push_time < time_stamp or last_push_time == 0:
                events.append(event["message"])
                if time_stamp > newest_push_time:
                    newest_push_time = time_stamp
            else:
                break

        if newest_push_time:
            self._update_last_push(device_id, newest_push_time)

        return events

    def send_push(self, data):
        assert isinstance(data, dict)
        assert 'start_time' in data
        assert 'end_time' in data
        assert 'message' in data

        event_list = List(self._key, db=self._redis)

        data['time_stamp'] = int(time.time())
        json_value = ujson.dumps(data)
        event_list = List(self._key, db=self._redis)
        event_list.lpush(json_value)

    def delete_push(self, *messages):

        event_list = List(self._key, db=self._redis)
        deleting = []
        for json_event in event_list.lrange(0, -1):
            event = ujson.loads(json_event)
            if event['message'] in messages:
                deleting.append(json_event)

        pipeline = self._redis.pipeline()
        event_list = List(self._key, pipeline=pipeline)
        for event in deleting:
            event_list.remove(event)
        pipeline.execute()
