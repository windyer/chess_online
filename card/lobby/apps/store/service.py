import uuid
import hashlib

import go.logging
from go.util import DotDict

from django.conf import settings

from card.core.error.common import CoreError
from card.core.charge import ITEMS

from card.lobby.aop import trace_service
from card.lobby.service.view_service import ViewService
from card.core.util.timestamp import get_timestamp_for_now
from card.lobby.extensions.logging import mongo_logger
from go.containers.containers import Hash,List
from card.lobby.apps.activity.base import ActivityHandler
from card.lobby.apps.store import models
from card.lobby.apps.player.models import PlayerExtra
from card.lobby.apps.store.store_event import StoreEvent
from card.core.util.lottery_key import LotteryFormula
from card.core.property.three import Property
from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.store.serializers import BullUrl
from go.containers import redis

@go.logging.class_wrapper
class StoreService(ViewService):

    def _get_item(self, item_id):
        if item_id in ITEMS.property_bags:
            item = ITEMS.property_bags[item_id]
        elif item_id in ITEMS.coins:
            item = ITEMS.coins[item_id]
        elif item_id in ITEMS.quick_coins:
            item = ITEMS.quick_coins[item_id]
        elif item_id in ITEMS.monthly_coins:
            item = ITEMS.monthly_coins[item_id]
        elif item_id in ITEMS.same_items:
            return self._get_item(ITEMS.same_items[item_id].item_id)
        else:
            return
        return item

    def _charge_log_to_mongo(self, user_id, item_id, count, channel, reason,
                             revenue=0, charge_place=None, charge_reason=None):
        
        item = self._get_item(item_id)
        if item is None:
            return
            
        item_info = item.copy()
        item_info.pop('name')
        item_info.pop('price')
        price = revenue or item.price

        extra = PlayerExtra.get_player_extra(user_id)
        timestamp = get_timestamp_for_now(unit='ms')
        mongo_logger.charge_statistics(
            user_id=user_id, item_id=item_id, count=count, price=price, channel=extra.channel,
            app_version=extra.app_version, reason=reason, item_info=None, 
            timestamp=get_timestamp_for_now(unit='ms'),
        )
        if 'coin' in item:
            mongo_logger.currency_issue(
                user_id=user_id, delta=item.coin, reason=reason,
                channel=channel, timestamp=timestamp,
                extra_info={'item_id': item_id, 'count': count}
            )
        if item_id in ITEMS.monthly_coins:
            mongo_logger.monthly_payment_subscribe(
                user_id=user_id, channel=channel, item_id=item_id,
                timestamp=timestamp
            )

    def purchase(self, user_id, item_id, count, reason, transaction_id=None, discount=None):
        property_service = self.service_repositories.db.property_service
        if transaction_id is None:
            transaction_id = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()
        if discount is None:
            discount = ActivityHandler.purchase_discount(user_id=user_id, 
                                service_repositories=self.service_repositories, 
                                activity_repository=self.activity_repository, 
                                context=DotDict({'item_id':item_id}))
        self.trans_logger.info('[user|%d] pre [purchase_item|%d] [count|%d] [reason|%s]'
            ' with [transaction|%s]', user_id, item_id, count, reason, transaction_id)
        response = property_service.purchase(user_id, transaction_id, item_id, count, discount)
        self.trans_logger.info('[user|%d] post [purchase_item|%d] [count|%d] [reason|%s]'
            ' with [transaction|%s]', user_id, item_id, count, reason, transaction_id)
        
        return response

    def charge(self, user_id, item_id, count, channel, reason, transaction_id=None,
               revenue=0, charge_place=None, charge_reason=None):
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        assert item_id in settings.STORE.charge_items
        assert count > 0
        assert revenue >= 0
        response = self.purchase(user_id, item_id, count, channel, transaction_id)
        ActivityHandler.process_charge(user_id=user_id,
                                service_repositories=self.service_repositories, 
                                activity_repository=self.activity_repository, 
                                context=DotDict({'item_id':item_id}))
        
        store_event = StoreEvent(self.service_repositories, self.activity_repository)
        store_event.send_charge_event(user_id, item_id)
        self._charge_log_to_mongo(user_id, org_id, count, channel, reason,
                                  revenue=revenue, charge_place=charge_place,
                                  charge_reason=charge_reason)
        lottery_count = 0
        extra = PlayerExtra.get_player_extra(user_id)
        if settings.LOTTERY.lottery_charge_enable and extra.app_version >= settings.LOTTERY.version:
            lottery_count = LotteryFormula.ProcessCharge(user_id, channel, item_id, count)

        if lottery_count != None and lottery_count > 0:
            property_service = self.service_repositories.db.property_service
            transaction_id = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()

            property_service.increment_item(user_id, transaction_id, Property.LOTTERY_TICKET.item_id, lottery_count)
            self.logger.debug("lottery_gain [user_id|%d] [delta|%d] [reason|%s]", user_id, lottery_count, "charge")
            try:
                player_service = PlayerService(self.service_repositories, self.activity_repository)
                items = player_service.get_property_items(user_id)
                total_count = 0
                for item in items:
                    if item['item_id'] == Property.LOTTERY_TICKET.item_id:                                        
                        total_count = item['count']
                        break

                bulletin_service = self.service_repositories.chat.bulletin_service
                bulletin_service.send_lottery_event(user_id=user_id, count=total_count, delta=lottery_count)
            except CoreError.CHAT_CONNECTION_FAILED:
                pass
        self.invite_awards(user_id,item_id)
        return response

    @trace_service
    def purchase_item(self, user_id, item_id, count):
        assert count > 0
        if item_id not in settings.STORE.purchase_items:
            raise CoreError.ITEM_COULD_NOT_BE_PURCHASED(item_id=item_id)

        response = self.purchase(user_id, item_id, count, 'purchase_item')

        extra = PlayerExtra.get_player_extra(user_id)
        cost = response.cost
        mongo_logger.currency_withdrawal(
            user_id=user_id, delta=cost, reason='purchase_item',
            channel=extra.channel,
            timestamp=get_timestamp_for_now(unit='ms'),
            extra_info={'item_id': item_id, 'count': count}
        )

        log         = models.StorePurchaseLog()
        log.user_id = user_id
        log.item_id = item_id
        log.count   = count
        log.cost    = cost
        log.save()

        return response

    @trace_service
    def sell_item(self, user_id, item_id, count):
        assert count > 0
        if item_id not in settings.STORE.sell_items:
            raise CoreError.ITEM_COULD_NOT_BE_SELL(item_id=item_id)
            
        property_service = self.service_repositories.db.property_service
        transaction_id = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()

        self.trans_logger.info('[user|%d] pre [sell_item|%d] [count|%d] [reason|%s]'
            ' with [transaction|%s]', user_id, item_id, count, "sell_item", transaction_id)
        response = property_service.sell(user_id, transaction_id, item_id, count)
        self.trans_logger.info('[user|%d] post [sell_item|%d] [count|%d] [reason|%s]'
            ' with [transaction|%s]', user_id, item_id, count, "sell_item", transaction_id)

        extra = PlayerExtra.get_player_extra(user_id)
        gain = response.gain
        mongo_logger.currency_issue(
            user_id=user_id, delta=gain, reason='sell_item',
            channel=extra.channel,
            timestamp=get_timestamp_for_now(unit='ms'),
            extra_info={'item_id': item_id, 'count': count}
        )

        log         = models.StoreSellLog()
        log.user_id = user_id
        log.item_id = item_id
        log.count   = count
        log.earn    = gain
        log.save()

        return response

    @trace_service
    def get_bull_url(self, user_id):
        extra = PlayerExtra.get_player_extra(user_id)
        channel = extra.channel
        channels = settings.BULL_URL.channels
        download = 'default'
        if channel in channels:
            download = channel
        url = settings.BULL_URL.base_url + channels[download].url
        url_front = settings.BULL_URL.second_base_url + channels[download].url_front
        packType = channels[download].packType
        packType_front = channels[download].packType_front
        """
        timestamp = get_timestamp_for_now(unit='ms')
        mongo_logger.bull_download(user_id=user_id, channel=channel, download=download, timestamp=timestamp)
        re = redis.Redis(**settings.PERSIST_REDIS)
        re.incr(settings.BULL_URL.download_count_key)
        """
        return {'url' : url, 'packType' : packType,'url_front' : url_front, 'packType_front' : packType_front}

    @trace_service
    def bull_complete(self, user_id):
        extra = PlayerExtra.get_player_extra(user_id)
        channel = extra.channel
        channels = settings.BULL_URL.channels
        download = 'default'
        if channel in channels:
            download = channel
        url = settings.BULL_URL.base_url + channels[download].url
        url_front = settings.BULL_URL.second_base_url + channels[download].url_front
        packType = channels[download].packType
        packType_front = channels[download].packType_front
        timestamp = get_timestamp_for_now(unit='ms')
        mongo_logger.bull_download(user_id=user_id, channel=channel, download=download, timestamp=timestamp)
        re = redis.Redis(**settings.PERSIST_REDIS)
        re.incr(settings.BULL_URL.download_count_key)

    @trace_service
    def invite_awards(self,user_id,item_id):
        re = redis.Redis(**settings.PERSIST_REDIS)
        key=settings.INVITE.redis_list_key.format(user_id)
        _listed = List(key, db=re)
        award_players = _listed.members
        item = self._get_item(item_id)
        print award_players
        try:
            if len(award_players)>=1:
                first_player = award_players[-1]
            else:
                return
            first_award = item.price * settings.INVITE.first_award_ratio
            first_key = settings.INVITE.redis_hash_key.format(first_player)
            first_hashed = Hash(first_key, db=re)
            get_first_award = first_hashed.hget('not_receive_award')
            if get_first_award is not None:
                first_award = int(first_award) +int(get_first_award)
            first_hashed.hset('not_receive_award',int(first_award))
        except:
            self.debug.info("[invite_awards] [user|%d] add [first_player] awards wrong",user_id)
            return
        try:
            if len(award_players)>=2:
                second_player = award_players[-2]
            else:
                return
            second_award = item.price * settings.INVITE.second_award_ratio
            second_key = settings.INVITE.redis_hash_key.format(second_player)
            second_hashed = Hash(second_key, db=re)
            get_second_award = second_hashed.hget('not_receive_award')
            if get_second_award is not None:
                second_award = int(second_award) +int(get_second_award)
            second_hashed.hset('not_receive_award', int(second_award))
        except:
            self.debug.info("[invite_awards] [user|%d] add [second_player] awards wrong", user_id)
            return
