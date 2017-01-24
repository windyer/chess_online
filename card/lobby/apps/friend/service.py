import uuid
import hashlib

from django.utils import timezone
from django.conf import settings
from django.core.exceptions import (ObjectDoesNotExist, MultipleObjectsReturned)
import time
import go.logging
from go.containers import redis
from card.core.error.common import CoreError
from card.core.error.lobby.friend_error import FriendError
from card.core.property.three import Property

from card.lobby.aop.logging import trace_service
from card.lobby.extensions.logging import mongo_logger
from card.core.util.timestamp import get_timestamp_for_now

from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.player.models import PlayerExtra,Player
from card.lobby.service.view_service import ViewService
from card.lobby.settings import activity
import models
from friend_event import FriendEvent
from card.core.enum import Vip

@go.logging.class_wrapper
class FriendService(ViewService):

    def _get_request_log(self, request_id):
        try:
            return models.FriendshipRequestLog.objects.get(pk=request_id)
        except (ObjectDoesNotExist):
            raise FriendError.NO_SUCH_REQUEST(request_id=request_id) 
        except MultipleObjectsReturned:
            assert False, "request_id can not be MultipleObjectsReturned"
            raise
        except Exception as ex:
            self.logger.exception(ex) 
            raise

    def check_friend_limit(self, user_id):
        social_service = self.service_repositories.db.social_service
        friend_count = social_service.get_friend_count(user_id).friend_count
        limit_count = settings.FRIEND.friend_count
        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        if profile.vip_title == Vip.SUPREMACY:
            limit_count = settings.FRIEND.supremacy_vip_friend_count
        if friend_count >= limit_count:
            raise FriendError.REACH_FRIEND_LIMIT(user_id=user_id, limit=limit_count)

    def already_friend(self, user_id, target_user_id):
        friend_service = self.service_repositories.db.social_service
        resp = friend_service.has_friendship(user_id, target_user_id)
        return resp.be_friend

    def get_friend_list(self, user_id):
        player_service = PlayerService(self.service_repositories, self.activity_repository)
        social_service = self.service_repositories.db.social_service
        friends_ids    = social_service.get_friends(user_id)

        friends_set = []
        friends_profiles = player_service.get_profiles(*friends_ids.users_id)
        for profile in friends_profiles:
            friends_set.append(profile._asdict())

        return friends_set

    @trace_service
    def make_friend(self, user_id, target_user_id, gift_id):
        #TODO: is the target user exist
        #TODO: some decorator
        if user_id == target_user_id:
            raise FriendError.MAKE_FRIEND_SELF(user_id=user_id)
        if self.already_friend(user_id, target_user_id):
            raise FriendError.ALREADY_FRIEND(user_id=user_id,
                                             target_user_id=target_user_id)

        player_extra = PlayerExtra.get_player_extra(user_id)
        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        cash = profile.currency + profile.bank_currency
        if cash <= settings.FRIEND.make_friend_currency_criterial:
            raise FriendError.MAKE_FRIEND_CURRENCY_LIMITATION(user_id=user_id)

        self.check_friend_limit(user_id)
        #self.check_friend_limit(target_user_id)
        
        #TODO:locals()
        request                = models.FriendshipRequestLog()
        request.user_id        = user_id
        request.target_user_id = target_user_id
        request.created_time   = timezone.now()
        request.gift_id        = gift_id
        request.save()

        transaction_id = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()
        self.trans_logger.info('[user|%d] pre make_friend send_gift [item|%d][count|%d] to '
                         '[receiver|%d] with [transaction|%s]',
                         user_id, gift_id, 1, target_user_id, transaction_id)
        social_service = self.service_repositories.db.social_service
        response = social_service.make_friend(request.id, user_id, target_user_id, 
                                      transaction_id, gift_id)
        self.trans_logger.info('[user|%d] post make_friend send_gift [item|%d][count|%d] to '
                         '[receiver|%d] with [transaction|%s]',
                         user_id, gift_id, 1, target_user_id, transaction_id)

        friend_event = FriendEvent(self.service_repositories, self.activity_repository)
        friend_event.send_gift_event(user_id, target_user_id, gift_id, 1)
        friend_event.send_make_friend_event(user_id, target_user_id,
                                            request.id, settings.PENDING)

        return response._asdict()

    def reply_request(self, user_id, target_user_id, request_id, status):
        #TODO: is the target user exist
        social_service = self.service_repositories.db.social_service
        request = self._get_request_log(request_id)
        request_status = request.status.upper()

        if target_user_id == user_id:
            raise FriendError.REPLY_FRIEND_SELF(user_id=user_id)
        if request_status == settings.ACCEPTED.upper():
            raise FriendError.ALREADY_FRIEND(user_id=user_id, target_user_id=target_user_id)
        elif request_status == settings.DECLINED.upper():
            raise FriendError.ALREADY_DECLINED(user_id=user_id, target_user_id=target_user_id)
        if status.upper() == settings.ACCEPTED.upper():
            self.check_friend_limit(user_id)

        request.status = status
        request.replied_time = timezone.now()
        request.save()
    
        status = status.upper()
        if status == settings.ACCEPTED.upper():
            social_service.accept_friend(user_id=user_id, target_user_id=target_user_id)
        elif status == settings.DECLINED.upper():
            social_service.decline_friend(user_id=user_id, target_user_id=target_user_id)

        friend_event = FriendEvent(self.service_repositories, self.activity_repository)
        friend_event.send_reply_friend_event(user_id, target_user_id, status)

        return request

    def break_friendship(self, user_id, target_user_id):
        #TODO: is the target user exist
        if user_id == target_user_id:
            raise FriendError.BREAK_FRIEND_SELF(user_id=user_id)
        if not self.already_friend(user_id, target_user_id):
            raise FriendError.NOT_FRIEND_YET(user_id=user_id, target_user_id=target_user_id)

        social_service       = self.service_repositories.db.social_service
        social_service.break_friend(user_id, target_user_id)

        friend_event = FriendEvent(self.service_repositories, self.activity_repository)
        friend_event.break_friendship(user_id, target_user_id)
        
        break_log            = models.FriendshipBreakLog()
        break_log.user_id    = user_id
        break_log.friend_user_id  = target_user_id
        break_log.break_time = timezone.now()
        break_log.save()
        return break_log

    @trace_service
    def send_currency(self, user_id, target_user_id, currency):
        #TODO: Aop for para check
        if user_id == target_user_id:
            raise FriendError.SEND_CURRENCY_SELF(user_id=user_id)
        if not self.already_friend(user_id, target_user_id):
            raise FriendError.NOT_FRIEND_YET(user_id=user_id,
                                         target_user_id=target_user_id)

        social_service  = self.service_repositories.db.social_service
        commission      = settings.FRIEND.cash_commission
        actual_currency = int(currency * (1 - commission))

        transaction_id = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()
        self.trans_logger.info('[user|%d] pre send_currency [currency|%d] to [friend|%d]'
                        '[actual_currency|%d] [commission|%f] with [transaction|%s]',
                         user_id, currency, target_user_id, actual_currency, 
                         commission, transaction_id)
        response = social_service.send_currency(user_id, target_user_id, transaction_id,
                                     currency, actual_currency)
        self.trans_logger.info('[user|%d] post send_currency [currency|%d] to [friend|%d]'
                        '[actual_currency|%d] [commission|%f] with [transaction|%s]',
                         user_id, currency, target_user_id, actual_currency, 
                         commission, transaction_id)
        
        extra = PlayerExtra.get_player_extra(user_id)
        mongo_logger.currency_withdrawal(
            user_id=user_id, delta=currency-actual_currency,
            reason='send_currency', channel=extra.channel,
            timestamp=get_timestamp_for_now(unit='ms'),
            extra_info={'target_user_id': target_user_id}
        )

        friend_event = FriendEvent(self.service_repositories, self.activity_repository)
        friend_event.send_currency_event(user_id, target_user_id, actual_currency)

        log                = models.SendCurrencyLog()
        log.user_id        = user_id
        log.target_user_id = target_user_id
        log.currency       = currency
        log.commission     = commission
        log.created_time   = timezone.now()
        log.save()

        return response._asdict()

    @trace_service
    def send_gift(self, user_id, target_user_id, item_id, count=1):
        if user_id == target_user_id:
            raise FriendError.SEND_GIFT_SELF(user_id=target_user_id)
        if item_id not in Property.send_items():
            raise CoreError.ITEM_COULD_NOT_BE_SENT(item_id=item_id)

        extra = PlayerExtra.get_player_extra(user_id)
        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        cash = profile.currency + profile.bank_currency
        if cash <= settings.FRIEND.send_gift_currency_criterial:
            raise FriendError.SEND_GIFT_CURRENCY_LIMITATION(user_id=user_id)

        social_service = self.service_repositories.db.social_service
        transaction_id = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()
        self.trans_logger.info('[user|%d] pre send_gift [item|%d] [count|%d] to '
                         '[receiver|%d] with [transaction|%s]',
                         user_id, item_id, count, target_user_id, transaction_id)
        response = social_service.send_gift(user_id, target_user_id, transaction_id, item_id, count)
        self.trans_logger.info('[user|%d] post send_gift [item|%d] [count|%d] to '
                         '[receiver|%d] with [transaction|%s]',
                         user_id, item_id, count, target_user_id, transaction_id)

        extra = PlayerExtra.get_player_extra(user_id)
        mongo_logger.currency_withdrawal(
            user_id=user_id, delta=Property.price(item_id),
            reason='send_gift', channel=extra.channel,
            timestamp=get_timestamp_for_now(unit='ms'),
            extra_info={'target_user_id': target_user_id,
                        'item_id': item_id, 'count': count}
        )

        friend_event = FriendEvent(self.service_repositories, self.activity_repository)
        friend_event.send_gift_event(user_id, target_user_id, item_id, count)

        log                = models.SendGiftLog()
        log.user_id        = user_id
        log.target_user_id = target_user_id
        log.item_id        = item_id
        log.count          = count
        log.created_time   = timezone.now()
        log.save()
        if activity.ACTIVITY['double_seventh']['double_seventh_logo']:
            self.set_date_gift(target_user_id,item_id,count)
        return response._asdict()

    def get_recommand_friend(self, user_id):
        return []

    def send_message(self, user_id, target_user_id, messages):
        if user_id == target_user_id:
            raise FriendError.SEND_MESSAGE_SELF(user_id=target_user_id)
        if not self.already_friend(user_id, target_user_id):
            raise FriendError.NOT_FRIEND_YET(user_id=user_id,
                                         target_user_id=target_user_id)
        
        friend_event = FriendEvent(self.service_repositories, self.activity_repository)
        friend_event.send_message(user_id, target_user_id, messages)

    def set_date_gift(self,target_user_id,item_id,count):
        if time.strftime("%Y%m%d", time.localtime(time.time())) == activity.ACTIVITY['double_seventh']['statistics_time'] :
            player = Player.get_player(target_user_id)
            re = redis.Redis(**settings.PERSIST_REDIS)
            currency=Property.price(item_id)*count
            if player.gender == 1 :
                re.zincrby('activity_male', target_user_id, currency)
            if player.gender == 2 :
                re.zincrby('activity_female', target_user_id, currency)