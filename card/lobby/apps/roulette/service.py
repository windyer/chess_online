from django.core.exceptions import (ObjectDoesNotExist, MultipleObjectsReturned)

from go.util import DotDict
from go.logging import class_wrapper

from card.core.conf import settings

from card.lobby.service.view_service import ViewService
from card.lobby.extensions.logging import mongo_logger
from card.core.util.timestamp import get_timestamp_for_now
from card.lobby.aop import (cache_roulette_record, 
                    trace_service, update_roulette_record)
from card.lobby.apps.store.service import StoreService
from card.lobby.apps.activity.base import ActivityHandler

from roulette_event import RouletteEvent
from card.lobby.apps.player.models import PlayerExtra
from card.lobby.apps.player.service import PlayerService
from card.core.error.lobby.roulette_error import RouletteError
from go.containers import redis
from go.containers.containers import Hash
from django.utils import timezone
import ujson
from card.core.util.timestamp import is_today
import time
from card.core.enum import RouletteType

import models
import utils
import go.logging
from card.core.util.lottery_key import LotteryFormula
from card.core.property.three import Property

@go.logging.class_wrapper
class RouletteService(ViewService):

    @update_roulette_record
    def _update_record(self,user_id, items):
        mysql_objects = []
        for item_id, item_count in items: 
            try:
                mysql_object = models.RouletteRecord.objects.get(
                                user_id=user_id, item_id=item_id)
            except ObjectDoesNotExist:
                mysql_object = models.RouletteRecord()
                mysql_object.item_id = item_id
                mysql_object.user_id = user_id
            except MultipleObjectsReturned:
                assert False, "user_id can not be MultipleObjectsReturned"
                raise
            except Exception as ex:
                self.logger.exception(ex) 
                raise

            try:
                mysql_object.item_count += item_count
                mysql_object.save()
            except Exception as ex:
                self.logger.exception(ex) 
                raise ex
            mysql_objects.append(mysql_object)

        return mysql_objects

    @cache_roulette_record
    def get_record(self, user_id):
        try:
            return models.RouletteRecord.objects.filter(user_id=user_id)
        except Exception as ex:
            self.logger.exception(ex) 
            raise

    @trace_service
    def get_next_roulette_type(self, user_id):
        player_extra = PlayerExtra.get_player_extra(user_id)

        re = redis.Redis(**settings.PERSIST_REDIS)
        key = settings.ROULETTE.roulette_history_key
        roulette_history_hash = Hash(key, re)
        self.logger.debug("roulette [user|%d] [device|%s] request roulette", user_id, player_extra.login_device_id)
        history = roulette_history_hash.hget(player_extra.login_device_id)
        if history is not None:
            history = ujson.loads(history)            
            if not is_today(history['roulette_time']) or not 'roulette_count' in history:
                return RouletteType.FREE
            elif history['roulette_count'] < settings.ROULETTE.free_count:
                return RouletteType.FREE
            elif history['roulette_count'] >= settings.ROULETTE.free_count and player_extra.created_today:
                return RouletteType.NONE
            return RouletteType.PAY
        return RouletteType.FREE

    @trace_service
    def roulette(self, user_id):
        player_extra = PlayerExtra.get_player_extra(user_id)

        re = redis.Redis(**settings.PERSIST_REDIS)
        key = settings.ROULETTE.roulette_history_key
        roulette_history_hash = Hash(key, re)
        self.logger.debug("roulette [user|%d] [device|%s] request roulette", user_id, player_extra.login_device_id)
        history = roulette_history_hash.hget(player_extra.login_device_id)
        discount = 0
        
        roulette_count = 0
        if history is not None:
            history = ujson.loads(history)
            if 'roulette_count' in history:
                roulette_count = history['roulette_count']
            if not is_today(history['roulette_time']):
                discount = 0
                roulette_count = 0
            elif roulette_count < settings.ROULETTE.free_count:
                discount = 0
            elif roulette_count >= settings.ROULETTE.free_count and player_extra.created_today:
                raise RouletteError.ROULETTE_NEWBIE_LIMITATION(user_id=user_id)
            else:
                discount = 1

        next_type = RouletteType.PAY
        if 0 == discount:
            roulette_type = RouletteType.FREE
            if player_extra.created_today:
                next_type = RouletteType.NONE
        else:
            roulette_type = RouletteType.PAY
        
        roulette_item = utils.RouletteProbController.get_random(roulette_type)
        count = 1
        while (roulette_item['item'].name == 'ROULETTE_LOTTERY_TICKET' ):
            roulette_item = utils.RouletteProbController.get_random(roulette_type)
            count = 1
        assert roulette_item is not None, 'roulette_item is None'


        routtle_item_id   = roulette_item.item.item_id
        store_service = StoreService(self.service_repositories, self.activity_repository)
        response = store_service.purchase(user_id, routtle_item_id, count, 'roulette', discount=discount)
        cost = response.cost

        self.logger.debug("roulette [user|%d] [device|%s] request roulette [discount|%d] [cost|%d]", user_id, player_extra.login_device_id, discount, cost)
        history = {"roulette_time":time.time(), "roulette_count":roulette_count + 1}
        roulette_history_hash.hset(player_extra.login_device_id, ujson.dumps(history))

        extra = PlayerExtra.get_player_extra(user_id)
        channel=extra.channel
        if 0 == discount:
            real_item = settings.ROULETTE.roulette_details[roulette_item.item].sub_item
        else:
            real_item = settings.ROULETTE.currency_roulette_details[roulette_item.item].sub_item
        mongo_logger.currency_withdrawal(
            user_id=user_id, delta=cost, reason='roulette',
            channel=channel, timestamp=get_timestamp_for_now(unit='ms'),
            extra_info={'item_id': routtle_item_id, 'count': 1,
                        'price': real_item.price}
        )

        if routtle_item_id == Property.LOTTERY_TICKET:
            LotteryFormula.addRouletteLotteryCount(user_id, channel, 1)
        
        roulette_log         = models.RouletteLog()
        roulette_log.user_id = user_id
        roulette_log.item_id = routtle_item_id
        roulette_log.name    = roulette_item.item.name
        roulette_log.count   = count
        roulette_log.cost    = roulette_item.item.price
        roulette_log.save()

        self._update_record(user_id, response.items)

        roulette_event = RouletteEvent(self.service_repositories)
        roulette_event.send_roulette_gift_event(user_id, routtle_item_id)
        """
        ActivityHandler.process_roulette(user_id=user_id, 
                                service_repositories=self.service_repositories, 
                                activity_repository=self.activity_repository, 
                                context=DotDict({'item_id':routtle_item_id}))
        """
        return (next_type, routtle_item_id, response)
