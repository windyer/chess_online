import random

import go.logging
from card.lobby.service.view_service import ViewService
from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.rank.service import RankService
from card.lobby.apps.timeline.serializers import EventSenderProfile
from card.lobby.apps.timeline.event_manager import (FriendTrend, 
                            FriendMessage, PersonalMessage,
                            TopSystemMessage, NormalSystemMessage,
                            SystemPush)

from django.conf import settings

@go.logging.class_wrapper
class TimeLineService(ViewService):
    
    def _append_sender_info(self, sender_ids, event_list, append_rank=False):
        sender_profiles = {}
        player_service = PlayerService(self.service_repositories, self.activity_repository)
        rank_service = RankService(self.service_repositories, self.activity_repository)
        user_profiles = player_service.get_profiles(*sender_ids)
        for profile in user_profiles:
            user_id = profile.user_id
            profile = profile._asdict()
            if append_rank:
                profile["ranks"] = rank_service.get_user_ranks(user_id)
            sender_info = EventSenderProfile(profile).data
            sender_profiles[user_id] = sender_info

        for item in event_list:
            sender_id = item['user_id']
            item['sender'] = sender_profiles[sender_id]     
            del item['user_id']

        return event_list

    def send_friend_trend(self, user_id, target_user_id, data):
        trend_manager = FriendTrend()
        trend_manager.send_event(user_id, target_user_id, data)

    def del_request_trend(self, user_id, target_user_id):
        trend_manager = FriendTrend()
        trend_manager.del_request_event(user_id, target_user_id)

    def get_friend_trends(self, user_id, page):
        trend_manager = FriendTrend()
        total_pages, events = trend_manager.get_events(user_id, page)

        sender_ids = set([])
        for event in events:
            sender_ids.add(event['user_id'])

        resp = {}
        resp['page'] = page
        resp['total_page'] = total_pages
        resp['events'] = self._append_sender_info(list(sender_ids), events, append_rank=True)
        return resp

    def send_friend_message(self, user_id, target_user_id, data):
        message_manager = FriendMessage()
        message_manager.send_event(user_id, target_user_id, data)

    def delete_friend_message(self, user_id, peer_user_id):
        message_manager = FriendMessage()
        message_manager.del_friend_message(user_id, peer_user_id)

    def get_friend_messages(self, user_id, peer_user_id, page):
        message_manager = FriendMessage()
        total_pages, messages = message_manager.get_events(
                                    user_id, peer_user_id, page)

        resp = {}
        resp['page'] = page
        resp['total_page'] = total_pages
        resp['events'] = self._append_sender_info((user_id, peer_user_id), messages)
        return resp

    def send_personal_message(self, user_id, message):
        personal_manager = PersonalMessage()
        personal_manager.send_event(user_id, {'message':message})

    def get_personal_message(self, user_id, page):
        personal_manager = PersonalMessage()
        total_pages, messages = personal_manager.get_events(user_id, page)

        resp = {}
        resp['page'] = page
        resp['total_page'] = total_pages
        resp['events'] = messages
        return resp

    def send_system_message(self, is_top, message):
        if is_top:
            system_manager = TopSystemMessage()
        else:
            system_manager = NormalSystemMessage()
        system_manager.send_message(message)

    def del_system_message(self, *messages):
        top_system_manager = TopSystemMessage()
        normal_system_manager = NormalSystemMessage()

        top_system_manager.del_message(*filter(lambda x: x['is_top'], messages))
        normal_system_manager.del_message(
            *filter(lambda x: not x['is_top'], messages)
        )

    def get_system_message(self, user_id):
        top_manager = TopSystemMessage()
        normal_manager = NormalSystemMessage()

        resp = {}
        resp['top'] = top_manager.get_events(user_id)
        resp['normal'] = normal_manager.get_events(user_id)
        return resp

    def get_all_system_message(self, user_id):
        top_manager = TopSystemMessage()
        normal_manager = NormalSystemMessage()

        resp = {}
        resp['top'] = top_manager.get_all_events(user_id)
        resp['normal'] = normal_manager.get_all_events(user_id)
        return resp

    def get_all_system_push(self):
        push_manager = SystemPush()
        return push_manager.get_all_push()

    def get_system_push(self, device_id):
        push_manager = SystemPush()
        next_time = int(random.gauss(*settings.TIME_LINE.push_interval.gauss))
        min_interval = settings.TIME_LINE.push_interval.min
        next_time = next_time if next_time > min_interval else min_interval

        resp = {}
        resp['next_time'] = next_time
        resp['messages'] = push_manager.get_push(device_id)
        return resp

    def send_system_push(self, data):
        push_manager = SystemPush()
        push_manager.send_push(data)

    def delete_system_push(self, *messages):
        push_manager = SystemPush()
        push_manager.delete_push(*messages)

    def reset_fetch_time(self, user_id):
        top_manager = TopSystemMessage()
        normal_manager = NormalSystemMessage()
        top_manager.reset_fetch_time(user_id)
        normal_manager.reset_fetch_time(user_id)
        personal_manager = PersonalMessage()
        personal_manager.reset_fetch_time(user_id)

    def reset_ttl_time(self, user_id):
        personal_manager = PersonalMessage()
        personal_manager.reset_ttl_time(user_id)

    def get_unread_info(self, user_id):
        message_manager = FriendMessage()
        trend_manager = FriendTrend()
        personal_manager = PersonalMessage()
        top_system = TopSystemMessage()
        normal_system = NormalSystemMessage()

        unread_system_count = top_system.unread_count(user_id) + normal_system.unread_count(user_id)

        resp = {}
        resp['friend_trend'] = trend_manager.unread_count(user_id)
        resp['friend_message'] = message_manager.unread_message_info(user_id)
        resp['personal_message'] = personal_manager.unread_count(user_id)
        resp['system_message'] = unread_system_count
        return resp

    def get_system_message_unread_info(self, user_id):
        top_system = TopSystemMessage()
        normal_system = NormalSystemMessage()

        unread_system_count = top_system.unread_count(user_id) + normal_system.unread_count(user_id)

        resp = {}
        resp['system_message'] = unread_system_count
        return resp
