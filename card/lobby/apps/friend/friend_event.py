from django.conf import settings

from card.core.property.three import Property
from card.core.error.common import CoreError

from card.api.task.timeline_service import TimelineService as PushService
from card.lobby.apps.timeline.service import TimeLineService
import card.lobby.apps.player.models as player_models

class FriendEvent(TimeLineService):

    def send_make_friend_event(self, user_id, target_user_id, request_id, status):
        data = {}
        data['user_id'] = user_id
        data['request_id'] = request_id
        data['status'] = status
        data['type'] = settings.REQUEST_FRIENDS_TRENDS_TYPE
        self.send_friend_trend(user_id=user_id, target_user_id=target_user_id, data=data)

        push_service = PushService()
        player_extra = player_models.PlayerExtra.get_player_extra(target_user_id)
        push_service.send_friend_request_event(user_id, target_user_id, player_extra.package_type)
       
    def send_reply_friend_event(self, user_id, target_user_id, status):
        data={}
        data['user_id'] = user_id
        data['status'] = status
        data['type'] = settings.MAKE_FRIENDS_TRENDS_TYPE
        self.send_friend_trend(user_id=user_id, target_user_id=target_user_id, data=data)
        self.del_request_trend(user_id=target_user_id, target_user_id=user_id)

    def send_currency_event(self,user_id, target_user_id, currency):
        data = {}
        data['user_id'] = user_id
        data['type'] = settings.SEND_CURRENCY_TRENDS_TYPE
        data['currency'] = currency
        self.send_friend_trend(user_id=user_id, target_user_id=target_user_id, data=data)

        push_service = PushService()
        player_extra = player_models.PlayerExtra.get_player_extra(target_user_id)
        push_service.send_currency_event(user_id, target_user_id, player_extra.package_type)

    def send_message(self, user_id, target_user_id, messages):
        data = {}
        data['user_id'] = user_id
        data['target_user_id'] = target_user_id
        data['type'] = settings.SEND_MESSAGE_TRENDS_TYPE
        data['messages'] = messages 
        self.send_friend_message(user_id=user_id, target_user_id=target_user_id, data=data)

        push_service = PushService()
        player_extra = player_models.PlayerExtra.get_player_extra(target_user_id)
        push_service.send_message_event(user_id, target_user_id, player_extra.package_type)

    def break_friendship(self, user_id, target_user_id):
        self.delete_friend_message(user_id, target_user_id)
        self.delete_friend_message(target_user_id, user_id)

    def send_gift_event(self, user_id, target_user_id, gift_id, count):
        data = {}
        data['user_id'] = user_id
        data['gift_id'] = gift_id
        data['count'] =count
        data['type'] = settings.SEND_GIFT_TRENDS_TYPE
        self.send_friend_trend(user_id=user_id, target_user_id=target_user_id, data=data)

        push_service = PushService()
        player_extra = player_models.PlayerExtra.get_player_extra(target_user_id)
        push_service.send_gift_event(user_id, target_user_id, player_extra.package_type)

        nick_name = ''
        target_nick_name = ''

        if gift_id == Property.RABBIT_GIRL.item_id or gift_id == Property.ROSES.item_id:
            player_service = self.service_repositories.db.player_service
            profiles = player_service.get_profiles(*(user_id, target_user_id)).profiles

            for profile in profiles:
                if profile.user_id == user_id:
                    nick_name = profile.nick_name
                else:
                    target_nick_name = profile.nick_name
                    
            try:
                bulletin_service = self.service_repositories.chat.bulletin_service
                bulletin_service.send_gift_event(user_id=user_id, nick_name=nick_name,  item_id=gift_id,
                                            target_nick_name=target_nick_name)
            except CoreError.CHAT_CONNECTION_FAILED:
                pass
        
        try:
            bulletin_service = self.service_repositories.chat.bulletin_service
            #bulletin_service.send_jackpot_charge_event(user_id=user_id, jackpot_award=award_currency)
            sender = nick_name[:]
            target = target_nick_name[:]
            max_len = settings.FRIEND.max_nick_name
            if player_extra.app_version < '2.0.0':
                send_rose_msg = settings.FRIEND.send_rose_msg
                send_rabbit_msg = settings.FRIEND.send_rabbit_msg
                if len(sender) > max_len:
                    sender = sender[0:max_len-3] + u'...'
                if len(target) > max_len:
                    target = target[0:max_len-3] + u'...'
            else:
                send_rose_msg = settings.FRIEND.new_send_rose_msg
                send_rabbit_msg = settings.FRIEND.new_send_rabbit_msg
            if gift_id == Property.RABBIT_GIRL.item_id:
                msg = send_rabbit_msg.format(sender.encode('utf-8'),target.encode('utf-8'))
                bulletin_service.send_urgent_event(text=msg.decode('utf-8'), duration=5,type=2)
            if gift_id == Property.ROSES.item_id:
                msg = send_rose_msg.format(sender.encode('utf-8'),target.encode('utf-8'))
                bulletin_service.send_urgent_event(text=msg.decode('utf-8'), duration=5,type=2)

        except CoreError.CHAT_CONNECTION_FAILED:
            pass
