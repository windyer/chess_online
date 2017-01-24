import time
import hashlib
import urllib
import urlparse
import thread
import ujson
import requests

from django.conf import settings

import go.logging

from card.core.error.lobby.zhuoyi_error import ZhuoyiError
from card.core.charge import ITEMS

from card.lobby.service.view_service import ViewService
from card.lobby.aop.logging import trace_service
from card.lobby.apps.store.service import StoreService
import card.lobby.apps.player.models as player_models
from card.lobby.apps.store.redis import ChargeStatus
from card.lobby.apps.player.service import PlayerService
from card.core.property.three import Property

from card.lobby.apps.zhuoyi import models as zhuoyi_models
from card.lobby.apps.zhuoyi.crypto import CryptoHelper
from card.lobby.settings import player
from card.core.error.lobby.player_error import PlayerError

coin_items = set( ITEMS.coins.keys() ).union( set( ITEMS.quick_coins.keys() ) )

@go.logging.class_wrapper
class ZhuoyiService(ViewService):

    def __init__(self, service_repositories, activity_repository):
        super(ZhuoyiService, self).__init__(service_repositories, activity_repository)

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
            raise ZhuoyiError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        return item

    def _create_cp_order(self, user_id, item_id, item, channel_id, app_id):
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        order_id = "{0}_{1}_{2}_{3}".format(user_id, org_id, int(time.time() * 1000000), thread.get_ident())
        charge_log = zhuoyi_models.ZhuoyiLog()
        charge_log.cporderid = order_id
        charge_log.appuserid = user_id
        charge_log.appid = app_id
        charge_log.waresid = settings.ZHUOYI.zhuoyi_items[item_id].pay_point_num
        charge_log.price = item.price
        charge_log.item_id = org_id
        charge_log.channel_id = channel_id
        charge_log.save()

        return charge_log
    @trace_service
    def process_charge_order(self, request_body, Recharge_Id, App_Id, Uin, Urecharge_Id, Recharge_Money, Extra, Recharge_Gold_Count, Pay_Status, Create_Time, Sign):
        str_request = 'App_Id={0}&Create_Time={1}&Extra={2}&Pay_Status={3}&Recharge_Gold_Count={4}&Recharge_Id={5}&Recharge_Money={6}&Uin={7}&Urecharge_Id={8}'.format(
                App_Id, Create_Time, Extra, Pay_Status, Recharge_Gold_Count, Recharge_Id, Recharge_Money, Uin, Urecharge_Id)
        check_sign = hashlib.md5(str_request + settings.ZHUOYI.app_conf[str(App_Id)].secret_key).hexdigest()
        if check_sign != Sign:
            raise ZhuoyiError.AUTH_ZHUOYI_NOTIFY_ORDER_SIGN_FAILED(transid=Recharge_Id, sign=Sign)

        order_id = Extra
        try:
            charge_log = zhuoyi_models.ZhuoyiLog.get_zhuoyi_log_by_orderid(order_id)
        except Exception:
            return "FAILURE"

        if charge_log is None:
            self.logger.info("[order_id|%s] is not exists in database", order_id)
            return "FAILURE"

        if charge_log.result == 1:
            self.logger.info("[order_id|%s] has been processed", order_id)
            return "SUCCESS"

        item_id = int(charge_log.item_id)
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        user_id = charge_log.appuserid
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        store_service = StoreService(self.service_repositories, self.activity_repository)
        store_service.charge(user_id, org_id, 1, charge_log.channel_id, 'charge', Recharge_Id, revenue=int(Recharge_Money))

        charge_status = ChargeStatus()
        charge_status.charge(user_id, item_id)

        #charge_log.transtype = transdata["transtype"]
        #charge_log.feetype = transdata["feetype"]
        charge_log.money = Recharge_Money
        #charge_log.currency = transdata["currency"]
        charge_log.result = Pay_Status
        charge_log.transtime = Create_Time
        #charge_log.cpprivate = transdata["cpprivate"]
        #charge_log.paytype = transdata["paytype"]
        charge_log.transid = Recharge_Id
        charge_log.save()
        try:
            player_charge = player_models.PlayerCharge.get_player_charge(user_id)
            money = player_charge.charge_money
            player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            player_charge.charge_money = money + Recharge_Money
            player_charge.save()
        except PlayerError.PLAYER_NOT_EXISTS:
            new_player_charge = player_models.PlayerCharge()
            new_player_charge.user_id = user_id
            new_player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            new_player_charge.charge_money = Recharge_Money
            new_player_charge.save()
        return "SUCCESS"

    @trace_service
    def process_charge_order_uuu(self, request_body, Recharge_Id, App_Id, Uin, Urecharge_Id, Recharge_Money, Extra,
                             Recharge_Gold_Count, Pay_Status, Create_Time, Sign):
        str_request = 'App_Id={0}&Create_Time={1}&Extra={2}&Pay_Status={3}&Recharge_Gold_Count={4}&Recharge_Id={5}&Recharge_Money={6}&Uin={7}&Urecharge_Id={8}'.format(
            App_Id, Create_Time, Extra, Pay_Status, Recharge_Gold_Count, Recharge_Id, Recharge_Money, Uin, Urecharge_Id)
        check_sign = hashlib.md5(str_request + settings.ZHUOYI.app_conf[str(App_Id)].secret_key).hexdigest()
        if check_sign != Sign:
            raise ZhuoyiError.AUTH_ZHUOYI_NOTIFY_ORDER_SIGN_FAILED(transid=Recharge_Id, sign=Sign)

        order_id = Urecharge_Id
        try:
            charge_log = zhuoyi_models.ZhuoyiLog.get_zhuoyi_log_by_orderid(order_id)
        except Exception:
            return "FAILURE"

        if charge_log is None:
            self.logger.info("[order_id|%s] is not exists in database", order_id)
            return "FAILURE"

        if charge_log.result == 1:
            self.logger.info("[order_id|%s] has been processed", order_id)
            return "SUCCESS"

        item_id = int(charge_log.item_id)
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        user_id = charge_log.appuserid
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        store_service = StoreService(self.service_repositories, self.activity_repository)
        store_service.charge(user_id, org_id, 1, charge_log.channel_id, 'charge', Recharge_Id,
                             revenue=int(Recharge_Money))

        charge_status = ChargeStatus()
        charge_status.charge(user_id, item_id)

        # charge_log.transtype = transdata["transtype"]
        # charge_log.feetype = transdata["feetype"]
        charge_log.money = int(Recharge_Money)
        # charge_log.currency = transdata["currency"]
        charge_log.result = int(Pay_Status)
        charge_log.transtime = int(Create_Time)
        # charge_log.cpprivate = transdata["cpprivate"]
        # charge_log.paytype = transdata["paytype"]
        charge_log.transid = Recharge_Id
        charge_log.save()
        try:
            player_charge = player_models.PlayerCharge.get_player_charge(user_id)
            money = player_charge.charge_money
            player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            player_charge.charge_money = money + int(Recharge_Money)
            player_charge.save()
        except PlayerError.PLAYER_NOT_EXISTS:
            new_player_charge = player_models.PlayerCharge()
            new_player_charge.user_id = user_id
            new_player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            new_player_charge.charge_money = int(Recharge_Money)
            new_player_charge.save()
        return "SUCCESS"

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
        if item_id not in settings.ZHUOYI.zhuoyi_items:
            raise ZhuoyiError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        item = self._get_purchase_item(user_id, item_id)

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        charge_status = ChargeStatus()
        if not charge_status.can_charge(user_id, profile.vip_title, item_id):
            raise ZhuoyiError.ITEM_HAS_CHARGED(user_id=user_id, item_id=item_id)

        app_id = str(app_id)
        notify_url = settings.ZHUOYI.app_conf[app_id].notify_url

        charge_log = self._create_cp_order(user_id, org_id, item, channel_id, app_id)

        pay_point = settings.ZHUOYI.zhuoyi_items[item_id].pay_point_num
        return {'transid':charge_log.cporderid, 'pay_point':pay_point, 'item_id':item_id, 'name':item.name, 'price':item.price}

    @trace_service
    def create_normal_charge_order(self, user_id, app_id, channel_id, item_id):
        return self.create_charge_order(user_id, channel_id, item_id, app_id)

    @trace_service
    def process_normal_charge_order(self, request_body, Recharge_Id, App_Id, Uin, Urecharge_Id, Recharge_Money, Extra, Recharge_Gold_Count, Pay_Status, Create_Time, Sign):
        return self.process_charge_order(request_body, Recharge_Id, App_Id, Uin, Urecharge_Id, Recharge_Money, Extra, Recharge_Gold_Count, Pay_Status, Create_Time, Sign)
