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

from django.conf import settings

import go.logging

from card.core.error.lobby.moguwan_error import MoguwanError

from card.core.charge import ITEMS

from card.lobby.service.view_service import ViewService
from card.lobby.aop.logging import trace_service
from card.lobby.apps.store.service import StoreService
import card.lobby.apps.player.models as player_models
from card.lobby.apps.store.redis import ChargeStatus
from card.lobby.apps.player.service import PlayerService
from card.core.property.three import Property
from card.lobby.apps.moguwan import models as moguwan_models
from card.lobby.settings import player
from card.core.error.lobby.player_error import PlayerError

@go.logging.class_wrapper
class MoguwanService(ViewService):

    def __init__(self, service_repositories, activity_repository):
        super(MoguwanService, self).__init__(service_repositories, activity_repository)

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
            raise MoguwanError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        return item

    def _create_cp_order(self, user_id, item_id, item, channel_id, app_id):
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        #md = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()
        order_id = "{0}_{1}_{2}_{3}".format(user_id, org_id, int(time.time() * 1000000), thread.get_ident())
        charge_log = moguwan_models.MoguwanLog()
        charge_log.cporderid = order_id
        charge_log.appuserid = user_id
        charge_log.appid = app_id
        charge_log.waresid = settings.MOGUWAN.moguwan_items[item_id].pay_point_num
        charge_log.price = item.price
        charge_log.item_id = org_id
        charge_log.channel_id = channel_id
        charge_log.save()

        return order_id

    def check_charge_order(self, transid):
        order_type = "1"
        app_id = settings.MOGUWAN.app_id
        secret_key = settings.MOGUWAN.secret_key
        sign = hashlib.md5(app_id + transid + secret_key).hexdigest()
        action = "10002"
        request_body={
            'AppID':app_id,
            'CooperatorOrderSerial':transid,
            'Sign':sign,
            'OrderType':order_type,
            'Action':action,
        }
        query_url = settings.MOGUWAN.query_order_url
        resp = requests.post(query_url, data=request_body)
        if resp is None or resp.content is None or resp.content == '':
            self.logger.debug("resp invalid")
            return
        js = json.loads(resp.content.decode('string-escape').strip('"'))
        recode = js["ResultCode"]
        content = urllib.unquote(js["Content"])
        sign = hashlib.md5(app_id + str(recode) + content + secret_key).hexdigest()
        if recode != 1 or js["Sign"] != sign or content == '':
            self.logger.debug("[transid|%s] [recode|%d] [sign|%s] [moguwan_sign|%s] [content|%s]", transid, recode,
                sign, js['Sign'], content)
            return
        content = base64.b64decode(content)
        content = json.loads(content)
        return content['OrderStatus']

    @trace_service
    def process_charge_order(self, user_id,out_trade_no, price, pay_status, extend, signType, sign):
        cporderid = extend
        s_sign = hashlib.md5(out_trade_no+price+pay_status+extend+settings.MOGUWAN.pay_key).hexdigest()
        if sign != s_sign:
            self.logger.debug('[moguwan_charge] [orderid|%s] [amount|%s] [sign|%s] [s_sign|%s] not match',
                              out_trade_no, price, sign, s_sign)
            return 'FAILED'
        if pay_status != '1':
            self.logger.debug('[moguwan_charge] [orderid|%s] [amount|%s] [status|%s] [extend|%s] failed',
                              out_trade_no, price, pay_status, extend)
            return 'FAILED'
        try:
            charge_log = moguwan_models.MoguwanLog.get_moguwan_log_by_cporderid(cporderid)
            if charge_log.result == 1:
                self.logger.info("[orderid|%s] [extend|%s] has been processed", out_trade_no, extend)
                return 'success'
        except Exception:
            self.logger.debug('[moguwan_charge] [orderid|%s] [amount|%s] [status|%s] [extend|%s] failed',
                              out_trade_no, price, pay_status, extend)
            return 'FAILED'

        if charge_log is None:
            self.logger.info("[orderid|%s] [extend|%s] is not exists in database", out_trade_no, extend)
            return 'FAILED'

        item_id = int(charge_log.item_id)
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        user_id = int(charge_log.appuserid)
        item = self._get_purchase_item(user_id, item_id)
        moguwan_amount = int(float(price))
        if item is None or item.price > moguwan_amount:
            self.logger.debug('[orderid|%s] [extend|%s] [amount|%s] [price|%d] not match',
                              out_trade_no, extend, price, item.price )
            return 'FAILED'
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        store_service = StoreService(self.service_repositories, self.activity_repository)
        store_service.charge(user_id, org_id, 1, charge_log.channel_id, 'charge', out_trade_no, revenue=moguwan_amount)

        charge_status = ChargeStatus()
        charge_status.charge(user_id, item_id)

        charge_log.money = moguwan_amount
        charge_log.result = 1
        charge_log.transtime = int(time.time())
        charge_log.transid = out_trade_no
        charge_log.save()
        try:
            player_charge=player_models.PlayerCharge.get_player_charge(user_id)
            money=player_charge.charge_money
            player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            player_charge.charge_money = money+moguwan_amount
            player_charge.save()
        except PlayerError.PLAYER_NOT_EXISTS:
            new_player_charge=player_models.PlayerCharge()
            new_player_charge.user_id=user_id
            new_player_charge.charge_times=time.strftime("%Y%m%d",time.localtime(time.time()))
            new_player_charge.charge_money=moguwan_amount
            new_player_charge.save()
        return 'success'

    @trace_service
    def create_charge_order(self, user_id, channel_id, item_id):
        try:
            player_charge = player_models.PlayerCharge.get_player_charge(user_id)
            money = player_charge.charge_money
            date= player_charge.charge_times
            if date != time.strftime("%Y%m%d",time.localtime(time.time())):
                player_charge.charge_money=0
                player_charge.save()
            if date == time.strftime("%Y%m%d",time.localtime(time.time())) and money >= player.PLAYER['charge_limit']and player.PLAYER['charge_limit']!=0:
                raise PlayerError.CHARGE_LIMIT(money=money)
        except PlayerError.PLAYER_NOT_EXISTS:
            pass
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        if item_id not in settings.MOGUWAN.moguwan_items:
            raise MoguwanError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        item = self._get_purchase_item(user_id, item_id)

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        charge_status = ChargeStatus()
        if not charge_status.can_charge(user_id, profile.vip_title, item_id):
            raise MoguwanError.ITEM_HAS_CHARGED(user_id=user_id, item_id=item_id)

        app_id = settings.MOGUWAN.app_id
        order_id = self._create_cp_order(user_id, org_id, item, channel_id, app_id)
        return {'cporderid':order_id, 'p_price':item.price*100, 'p_desc':item.name, 'p_name':item.name}
