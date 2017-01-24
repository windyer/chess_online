#coding=utf-8
import time
import hashlib
import uuid
import urllib
import urlparse
import thread
import ujson
import requests
import base64
import json
import urllib2
import hmac
from django.conf import settings

import go.logging

from card.core.error.lobby.dianxin_error import DianxinError
from card.core.charge import ITEMS

from card.lobby.service.view_service import ViewService
from card.lobby.aop.logging import trace_service
from card.lobby.apps.store.service import StoreService
import card.lobby.apps.player.models as player_models
from card.lobby.apps.store.redis import ChargeStatus
from card.lobby.apps.player.service import PlayerService
from card.core.property.three import Property

from card.lobby.apps.dianxin import models as dianxin_models
from card.core.error.lobby.player_error import PlayerError
from card.lobby.settings import player



@go.logging.class_wrapper
class DianxinService(ViewService):

    def __init__(self, service_repositories, activity_repository):
        super(DianxinService, self).__init__(service_repositories, activity_repository)

    def _get_purchase_item(self, user_id, item_id):
        if item_id in ITEMS.coins:
            item = ITEMS.coins[item_id]
        elif item_id in ITEMS.quick_coins:
            item = ITEMS.quick_coins[item_id]
        elif item_id in ITEMS.property_bags:
            item = ITEMS.property_bags[item_id]
        elif item_id in ITEMS.same_items:
            other_id = ITEMS.same_items[item_id].item_id
            return self._get_purchase_item(user_id, other_id)
        else:
            raise DianxinError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        return item

    def _create_cp_order(self, user_id, item_id, item, channel_id, app_id):
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        #md = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()
        order_id = "{0}_{1}_{2}".format(user_id, org_id, int(time.time() * 100000000))
        charge_log = dianxin_models.DianxinLog()
        charge_log.cporderid = order_id
        charge_log.appuserid = user_id
        charge_log.appid = app_id
        charge_log.waresid = settings.DIANXIN.dianxin_items[item_id].pay_point_num
        charge_log.price = item.price
        charge_log.item_id = org_id
        charge_log.channel_id = channel_id
        charge_log.save()

        return charge_log

    def check_charge_order(self, transid):
        order_type = "1"
        app_id = settings.DIANXIN.app_id
        secret_key = settings.DIANXIN.secret_key
        sign = hashlib.md5(app_id + transid + secret_key).hexdigest()
        action = "10002"
        request_body={
            'AppID':app_id,
            'CooperatorOrderSerial':transid,
            'Sign':sign,
            'OrderType':order_type,
            'Action':action,
        }
        query_url = settings.DIANXIN.query_order_url
        resp = requests.post(query_url, data=request_body)
        if resp is None or resp.content is None or resp.content == '':
            self.logger.debug("resp invalid")
            return
        js = json.loads(resp.content.decode('string-escape').strip('"'))
        recode = js["ResultCode"]
        content = urllib.unquote(js["Content"])
        sign = hashlib.md5(app_id + str(recode) + content + secret_key).hexdigest()
        if recode != 1 or js["Sign"] != sign or content == '':
            self.logger.debug("[transid|%s] [recode|%d] [sign|%s] [baid_sign|%s] [content|%s]", transid, recode,
                sign, js['Sign'], content)
            return
        content = base64.b64decode(content)
        content = json.loads(content)
        return content['OrderStatus']

    @trace_service
    def process_charge_order(self, cp_order_id,correlator,result_code,fee,pay_type,method,sign,version):
        app_key=settings.DIANXIN.app_key
        src = cp_order_id+correlator+result_code+str(fee)+pay_type+method+app_key
        m2 = hashlib.md5()
        m2.update(src)
        s_sign = m2.hexdigest()
        if result_code != '00':
            self.logger.debug(
                '[dianxin_charge] [orderid|%s] [amount|%s]  [result_code|%s]   wrong',
                cp_order_id, fee, result_code)
            return {'OrderId' :cp_order_id,'ResponseCode':1}
        if sign != s_sign:
            self.logger.debug(
                '[dianxin_charge] [orderid|%s] [amount|%s]  [sign|%s] [s_sign|%s]  not match',
                cp_order_id, fee,  sign, s_sign)
            return {'OrderId' :cp_order_id,'ResponseCode':1}
        try:
            charge_log = dianxin_models.DianxinLog.get_dianxin_log_by_transid(cp_order_id)
            if charge_log.result == 1:
                self.logger.debug(
                    '[dianxin_charge] [orderid|%s] [amount|%s]  [other_id|%s] already exist',
                    cp_order_id, fee, charge_log.id)
                return {'OrderId' :cp_order_id,'ResponseCode':1}
        except Exception:
            return {'OrderId' :cp_order_id,'ResponseCode':1}

        if charge_log is None:
            self.logger.info("[orderid|%s]  is not exists in database", cp_order_id)
            return {'OrderId' :cp_order_id,'ResponseCode':1}
        if charge_log.result > 0:
            self.logger.info("[transid|%s] has been processed", cp_order_id)
            return {'OrderId' :cp_order_id,'ResponseCode':0}

        item_id = int(charge_log.item_id)
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        user_id = int(charge_log.appuserid)
        item = self._get_purchase_item(user_id, item_id)
        dianxin_amount = int(fee)
        if item is None or item.price > dianxin_amount:
            self.logger.debug('[orderid|%s] [amount|%s] [price|%d] not match',
                              cp_order_id, fee, item.price)
            return {'OrderId' :cp_order_id,'ResponseCode':0}
        #player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        store_service = StoreService(self.service_repositories, self.activity_repository)
        store_service.charge(user_id, org_id, 1, charge_log.channel_id, 'charge', cp_order_id,
                             revenue=int(dianxin_amount))

        charge_status = ChargeStatus()
        charge_status.charge(user_id, item_id)

        charge_log.money = dianxin_amount
        charge_log.result = 1
        charge_log.transtime = int(time.time())
        charge_log.transid = cp_order_id
        charge_log.save()
        try:
            player_charge = player_models.PlayerCharge.get_player_charge(user_id)
            money = player_charge.charge_money
            player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            player_charge.charge_money = money + dianxin_amount
            player_charge.save()
        except PlayerError.PLAYER_NOT_EXISTS:
            new_player_charge = player_models.PlayerCharge()
            new_player_charge.user_id = user_id
            new_player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            new_player_charge.charge_money = dianxin_amount
            new_player_charge.save()
        return {'OrderId' :cp_order_id,'ResponseCode':0}


    @trace_service
    def create_charge_order(self, user_id, channel_id, item_id):
        try:
            player_charge = player_models.PlayerCharge.get_player_charge(user_id)
            money = player_charge.charge_money
            date = player_charge.charge_times
            if date != time.strftime("%Y%m%d", time.localtime(time.time())):
                player_charge.charge_money = 0
                player_charge.save()
            if date == time.strftime("%Y%m%d", time.localtime(time.time())) and money >= player.PLAYER[
                'charge_limit']and player.PLAYER['charge_limit']!=0:
                raise PlayerError.CHARGE_LIMIT(money=money)
        except PlayerError.PLAYER_NOT_EXISTS:
            pass
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        if item_id not in settings.DIANXIN.dianxin_items:
            raise DianxinError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        item = self._get_purchase_item(user_id, item_id)

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        charge_status = ChargeStatus()
        if not charge_status.can_charge(user_id, profile.vip_title, item_id):
            raise DianxinError.ITEM_HAS_CHARGED(user_id=user_id, item_id=item_id)
        app_id = settings.DIANXIN.app_id
        app_key = settings.DIANXIN.app_key
        charge_log = self._create_cp_order(user_id, org_id, item, channel_id, app_id)
        charge_log.transid = charge_log.cporderid
        charge_log.save()
        src = charge_log.transid + str(item.price) + app_key
        m2 = hashlib.md5()
        m2.update(src)
        sign = m2.hexdigest()
        return {'transid':charge_log.transid,'price':item.price, 'sign':sign}
