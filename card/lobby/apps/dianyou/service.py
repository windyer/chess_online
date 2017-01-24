#coding=utf-8
import time
import hashlib

import thread
import requests
import crypto
import json

from django.conf import settings

import go.logging

from card.core.error.lobby.dianyou_error import DianyouError
from card.core.charge import ITEMS

from card.lobby.service.view_service import ViewService
from card.lobby.aop.logging import trace_service
from card.lobby.apps.store.service import StoreService
import card.lobby.apps.player.models as player_models
from card.lobby.apps.store.redis import ChargeStatus
from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.dianyou import models as dianyou_models
from card.core.error.lobby.player_error import PlayerError
from card.lobby.settings import player



@go.logging.class_wrapper
class DianyouService(ViewService):

    def __init__(self, service_repositories, activity_repository):
        super(DianyouService, self).__init__(service_repositories, activity_repository)

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
            raise DianyouError.item_not_exist(user_id=user_id, item_id=item_id)
        return item

    def _create_cp_order(self, user_id, item_id, item, channel_id, app_id):
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        #md = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()
        order_id = "{0}_{1}_{2}_{3}".format(user_id, org_id, int(time.time() * 1000000), thread.get_ident())
        charge_log = dianyou_models.DianyouLog()
        charge_log.cporderid = order_id
        charge_log.appuserid = user_id
        charge_log.appid = app_id
        charge_log.waresid = settings.DIANYOU.dianyou_items[item_id].pay_point_num
        charge_log.price = item.price
        charge_log.item_id = org_id
        charge_log.channel_id = channel_id
        charge_log.save()

        return charge_log

    def check_charge_order(self, transid):
        app_id = settings.DIANYOU  .app_id
        app_key = settings.DIANYOU.app_key
        sign = hashlib.md5(app_id + transid + app_key).hexdigest()
        request_body={
            'game_id':app_id,
            'cp_trade_no':transid,
            'sign':sign,
        }
        query_url = settings.DIANYOU.query_order_url
        resp = requests.post(query_url, data=request_body)
        if resp is None or resp.content is None or resp.content == '':
            self.logger.debug("resp invalid")
            return
        js = json.loads(resp.content.decode('string-escape').strip('"'))
        return js['data']

    @trace_service
    def process_charge_order(self,data):
        cp_trade_no = data['ssid']
        uid = data['uid']
        total_fee = data['fee']
        pay_status = data['st']
        sign = data['sign']
        game_secure_key=settings.DIANYOU.PayKey
        s_sign = crypto.verify_sign(data,game_secure_key)
        if not s_sign:
            self.logger.debug(
                '[dianyou_charge] [orderid|%s] [amount|%s]  [sign|%s] [s_sign|%s]  not match',
                cp_trade_no, total_fee,  sign, s_sign)
            return {'status':'failed', 'desc':'sign wrong'}
        try:
            charge_log = dianyou_models.DianyouLog.get_dianyou_log_by_transid(cp_trade_no)
            if charge_log.result == 1:
                self.logger.debug(
                    '[dianyou_charge] [orderid|%s] [amount|%s]  [other_id|%s] already exist',
                    cp_trade_no, total_fee, charge_log.id)
                return {'status':'failed', 'desc':'order already exist'}
        except Exception:
            return {'status': 'failed', 'desc': 'order wromg'}

        if charge_log is None:
            self.logger.info("[orderid|%s]  is not exists in database", cp_trade_no)
            return {'status':'failed', 'desc':'no order'}

        item_id = int(charge_log.item_id)
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        user_id = int(charge_log.appuserid)
        item = self._get_purchase_item(user_id, item_id)
        dianyou_amount = int(total_fee.strip())
        if item is None or item.price*100  > dianyou_amount:
            self.logger.debug('[orderid|%s] [amount|%s] [price|%d] not match',
                              cp_trade_no, total_fee, item.price * 100)
            return {'status':'failed', 'desc':'order wrong'}
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        store_service = StoreService(self.service_repositories, self.activity_repository)
        store_service.charge(user_id, org_id, 1, charge_log.channel_id, 'charge', cp_trade_no,
                             revenue=int(dianyou_amount/100 ))

        charge_status = ChargeStatus()
        charge_status.charge(user_id, item_id)

        charge_log.money = dianyou_amount/100
        charge_log.result = 1
        charge_log.transtime = int(time.time())
        charge_log.transid = cp_trade_no
        charge_log.save()
        try:
            player_charge = player_models.PlayerCharge.get_player_charge(user_id)
            money = player_charge.charge_money
            player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            player_charge.charge_money = money + dianyou_amount
            player_charge.save()
        except PlayerError.PLAYER_NOT_EXISTS:
            new_player_charge = player_models.PlayerCharge()
            new_player_charge.user_id = user_id
            new_player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            new_player_charge.charge_money = dianyou_amount
            new_player_charge.save()
        return {'success'}

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
        if item_id not in settings.DIANYOU.dianyou_items:
            raise DianyouError.item_not_exist(user_id=user_id, item_id=item_id)
        item = self._get_purchase_item(user_id, item_id)

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        charge_status = ChargeStatus()
        if not charge_status.can_charge(user_id, profile.vip_title, item_id):
            raise DianyouError.item_has_charged(user_id=user_id, item_id=item_id)

        app_id = settings.DIANYOU.app_id
        charge_log = self._create_cp_order(user_id, org_id, item, channel_id, app_id)
        charge_log.transid = charge_log.cporderid
        charge_log.save()


        return {'transid':charge_log.transid,'callbackurl':settings.DIANYOU.notify_url,'price':item.price, 'name':item.name}
