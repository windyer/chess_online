import time
import hashlib
import urllib
import urlparse
import thread
import ujson
import requests
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA 
from Crypto.Hash import SHA
import base64

from django.conf import settings

import go.logging

from card.core.error.lobby.wiipay_error import WiipayError
from card.core.charge import ITEMS

from card.lobby.service.view_service import ViewService
from card.lobby.aop.logging import trace_service
from card.lobby.apps.store.service import StoreService
import card.lobby.apps.player.models as player_models
from card.lobby.apps.store.redis import ChargeStatus
from card.lobby.apps.player.service import PlayerService
from card.core.property.three import Property

from card.lobby.apps.wiipay import models as wiipay_models
from card.lobby.apps.wiipay.crypto import CryptoHelper
from Crypto.PublicKey import RSA
from card.lobby.settings import player
from card.core.error.lobby.player_error import PlayerError

coin_items = set( ITEMS.coins.keys() ).union( set( ITEMS.quick_coins.keys() ) )

@go.logging.class_wrapper
class WiiPayService(ViewService):

    def __init__(self, service_repositories, activity_repository):
        super(WiiPayService, self).__init__(service_repositories, activity_repository)

        self.pub_keys = {}
        for app_id in settings.WIIPAY.app_conf:
            key = RSA.importKey(settings.WIIPAY.app_conf[app_id].pubkey)
            self.pub_keys[app_id] = PKCS1_v1_5.new(key)

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
            raise WiipayError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        return item

    def _create_cp_order(self, user_id, item_id, item, channel_id, app_id):
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        order_id = "{0}_{1}_{2}_{3}".format(user_id, org_id, int(time.time() * 1000000), thread.get_ident())
        charge_log = wiipay_models.WiipayLog()
        charge_log.cporderid = order_id
        charge_log.appuserid = user_id
        charge_log.appid = app_id
        charge_log.waresid = int(settings.WIIPAY.wiipay_items[item_id].pay_point_num)
        charge_log.price = item.price
        charge_log.item_id = org_id
        charge_log.channel_id = channel_id
        charge_log.save()

        return charge_log

    @trace_service
    def process_charge_order(self, request_body, app_id, operatorType, operatorTypeTile, 
        channelCode, appCode, payCode, imsi, tel, state, price, bookNo, date, devPrivate, 
        synType, sig):
        if not app_id in settings.WIIPAY.app_conf:
            raise WiipayError.AUTH_WIIPAY_NOTIFY_ORDER_FAILED(transdata=bookNo, sign=sig)

        content = "operatorType={0}&operatorTypeTile={1}&channelCode={2}&appCode={3}&payCode={4}&imsi={5}&tel={6}&state={7}&price={8}&bookNo={9}&date={10}&devPrivate={11}&synType={12}".format(
            operatorType, operatorTypeTile.encode('utf-8'), channelCode, appCode, payCode, imsi, tel, state, price, bookNo, date, devPrivate, synType)
        self_sign = SHA.new(content)
        sign = base64.b64decode(sig)
        if not self.pub_keys[app_id].verify(self_sign, sign):
            raise WiipayError.AUTH_WIIPAY_NOTIFY_ORDER_FAILED(transdata=bookNo, sign=sig)

        transdata = ujson.loads(base64.b64decode(devPrivate))
        try:
            charge_log = wiipay_models.WiipayLog.get_wiipay_log_by_cporderid(transdata["order_id"])
        except Exception:
            return "failure"

        if charge_log is None:
            self.logger.info("[transdata|%s] of [transid|%s] is not exists in database", bookNo, transdata["order_id"])
            return "failure"

        if charge_log.result <= 0:
            self.logger.info("[transdata|%s] of [transid|%s] has been processed", bookNo, transdata["order_id"])
            return "success"

        if state.lower() != 'success':
            self.logger.info("[wiipay|%s] [state|%s] [order_id|%s]", bookNo, state, charge_log.cporderid)
            return 'success'

        item_id = int(charge_log.item_id)
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        user_id = charge_log.appuserid
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        store_service = StoreService(self.service_repositories, self.activity_repository)
        store_service.charge(user_id, org_id, 1, charge_log.channel_id, 'charge', transdata["order_id"], revenue=int(price))

        charge_status = ChargeStatus()
        charge_status.charge(user_id, item_id)

        charge_log.operator_type = operatorType
        charge_log.syn_type = synType
        charge_log.money = price
        charge_log.result = 0
        charge_log.transtime = date
        charge_log.transid = bookNo
        charge_log.channel_code = channelCode
        charge_log.app_code = appCode
        charge_log.pay_code = payCode
        charge_log.save()
        try:
            player_charge = player_models.PlayerCharge.get_player_charge(user_id)
            money = player_charge.charge_money
            player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            player_charge.charge_money = money + price
            player_charge.save()
        except PlayerError.PLAYER_NOT_EXISTS:
            new_player_charge = player_models.PlayerCharge()
            new_player_charge.user_id = user_id
            new_player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            new_player_charge.charge_money = price
            new_player_charge.save()
        return "success"

    @trace_service
    def create_charge_order(self, user_id, channel_id, item_id, app_id):
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
        if item_id not in settings.WIIPAY.wiipay_items:
            raise WiipayError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        item = self._get_purchase_item(user_id, item_id)

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        charge_status = ChargeStatus()
        if not charge_status.can_charge(user_id, profile.vip_title, item_id):
            raise WiipayError.ITEM_HAS_CHARGED(user_id=user_id, item_id=item_id)

        if not app_id in settings.WIIPAY.app_conf:
            raise WiipayError.APP_ID_INVALIDE(app_id=app_id)
        
        notify_url = settings.WIIPAY.app_conf[app_id].notify_url

        charge_log = self._create_cp_order(user_id, org_id, item, channel_id, app_id)
        pay_point = settings.WIIPAY.wiipay_items[item_id].pay_point_num
        return {'order_id':charge_log.cporderid, 'pay_point':pay_point, 'item_id':org_id, 'name':item.name, 'price':item.price}
