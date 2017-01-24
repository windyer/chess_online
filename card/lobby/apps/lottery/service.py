from django.core.exceptions import (ObjectDoesNotExist, MultipleObjectsReturned)

from go.util import DotDict
from go.logging import class_wrapper

from card.core.conf import settings

from card.lobby.service.view_service import ViewService
from card.lobby.extensions.logging import mongo_logger
from card.core.util.timestamp import get_timestamp_for_now

from card.lobby.apps.store.service import StoreService
from card.lobby.apps.activity.base import ActivityHandler

from card.lobby.apps.player.models import PlayerExtra
from card.lobby.apps.player.service import PlayerService
from go.containers import redis
from go.containers.containers import Hash
from django.utils import timezone
import ujson
from card.core.util.timestamp import is_today
import time

import models
import go.logging
from card.core.util.lottery_key import LotteryFormula
from card.core.property.three import Property
from card.lobby.aop.logging import trace_service
import uuid
import hashlib
import datetime

@go.logging.class_wrapper
class LotteryService(ViewService):

    def _update_record(self,user_id, item_id, count, number=None, is_handled=False, gm_name=None):
        mysql_object = models.LotteryRecord()
        mysql_object.item_id = item_id
        mysql_object.user_id = user_id
        mysql_object.count = count
        mysql_object.is_handled = is_handled
        if not gm_name is None:
            mysql_object.gm_name = gm_name
        if not number is None:
            mysql_object.number = number

        try:            
            mysql_object.save()
        except Exception as ex:
            self.logger.exception(ex) 
            raise ex

        return mysql_object

    def get_unhandle_lottery(self):
        mysql_objects = models.LotteryRecord.objects.filter(is_handled=False)
        return mysql_objects

    def handle_lottery(self, id, gm_name, sn):
        try:
            mysql_object = models.LotteryRecord.objects.get(id=id)
        except Exception as ex:
            self.logger.exception(ex) 
            raise ex
        try:
            mysql_object.is_handled = True
            mysql_object.gm_name = True
            mysql_object.handle_time = datetime.datetime.now()
            mysql_object.handle_sn = sn
            mysql_object.save()
        except Exception as ex:
            self.logger.exception(ex) 
            raise ex

    def _exchange_item(self, conf, user_id, item_id, count):                
        property_service = self.service_repositories.db.property_service
        transaction_id = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()
        consume = conf['consume'] * count
        result = property_service.decrement_item(user_id, transaction_id, Property.LOTTERY_TICKET.item_id, consume)
        self.logger.debug("lottery_consume [user_id|%d] [delta|%d] [item_id|%d]", user_id, consume, item_id)
        return result

    def get_latest_exchage(self):
        response = []
        try:
            max_id = models.LotteryRecord.objects.latest('user_id').id
            objects = models.LotteryRecord.objects.filter(id__gt = max_id - settings.LOTTERY.latest_count)
            player_service = PlayerService(self.service_repositories, self.activity_repository)
            for obj in objects:
                profile = player_service.get_profile(obj.user_id)
                response.append({"uer_id":obj.user_id, 'timestamp':time.mktime(obj.create_time.timetuple()), 
                    'item_id':obj.item_id, 'nick_name':profile.nick_name})
        except Exception as ex:
            self.logger.exception(ex) 
            pass
        return response


    @trace_service
    def lottery_item(self, user_id, item_id, count):
        if item_id not in settings.LOTTERY.lottery_items:
            self.logger.debug("LotteryService.lottery_item [user_id|%d] [item_id|%d] not in settings", user_id, item_id)
            return
        conf = settings.LOTTERY.lottery_items[item_id]
        result = self._exchange_item(conf, user_id, item_id, count)
        response = {}
        player_service = PlayerService(self.service_repositories, self.activity_repository)
        items = player_service.get_property_items(user_id)
        for item in items:
            if item['item_id'] == Property.LOTTERY_TICKET.item_id:                
                response[Property.LOTTERY_TICKET.item_id] = item['count']
                break

        if result:
            transaction_id = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()
            consume = conf['consume'] * count
            if conf.sub_item == Property.CAT_FOOD.item_id:
                store_service = StoreService(self.service_repositories, self.activity_repository)
                res = store_service.purchase(user_id, Property.CAT_FOOD.item_id, count, 'lottery', discount=0)
                response['cat_weight'] = res.cat_weight
            else:                
                res = player_service.increment_currency(user_id, conf.count, "lottery")
                response['currency'] = res.currency

            self._update_record(user_id, item_id, count, True, "system")
            return response

    @trace_service
    def lottery_phone(self, user_id, phone_number, item_id, count):
        if item_id not in settings.LOTTERY.phone_items:
            self.logger.debug("LotteryService.lottery_item [user_id|%d] [item_id|%d] not in settings", user_id, item_id)
            return
        if len(phone_number) != settings.LOTTERY.phone_number_len:
            self.logger.debug("LotteryService.lottery_item [user_id|%d] [phone_number|%s] invalid", user_id, phone_number)
        conf = settings.LOTTERY.phone_items[item_id]
        result = self._exchange_item(conf, user_id, item_id, count)
        response = {}
        player_service = PlayerService(self.service_repositories, self.activity_repository)
        items = player_service.get_property_items(user_id)
        for item in items:
            if item['item_id'] == Property.LOTTERY_TICKET.item_id:                
                response[Property.LOTTERY_TICKET.item_id] = item['count']
                break
        if result:
            self._update_record(user_id, item_id, count, phone_number)
        return response

    @trace_service
    def lottery_qq(self, user_id, qq_number, item_id, count):
        if item_id not in settings.LOTTERY.qq_items:
            self.logger.debug("LotteryService.lottery_item [user_id|%d] [item_id|%d] not in settings", user_id, item_id)
            return
        l = len(qq_number)
        if l < settings.LOTTERY.qq_number_len_min or l > settings.LOTTERY.qq_number_len_max:
            self.logger.debug("LotteryService.lottery_item [user_id|%d] [qq_number|%s] invalid", user_id, qq_number)
        conf = settings.LOTTERY.qq_items[item_id]
        result = self._exchange_item(conf, user_id, item_id, count)
        response = {}
        player_service = PlayerService(self.service_repositories, self.activity_repository)
        items = player_service.get_property_items(user_id)
        for item in items:
            if item['item_id'] == Property.LOTTERY_TICKET.item_id:                
                response[Property.LOTTERY_TICKET.item_id] = item['count']
                break
        if result:
            self._update_record(user_id, item_id, count, qq_number)
        return response