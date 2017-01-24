import time
import hashlib
import ujson

import go.logging

from card.core.charge import ITEMS

from django.conf import settings
from card.lobby.service.view_service import ViewService
from card.lobby.aop.logging import trace_service
import card.lobby.apps.player.models as player_models
from card.lobby.apps.mobile import models as mobile_models
from card.lobby.apps.store.service import StoreService
from card.lobby.apps.store.redis import ChargeStatus

@go.logging.class_wrapper
class MobileService(ViewService):

    def _check_sign(self, OrderID, ChannelID, PayCode, MD5Sign):
        app_key = settings.MOBILE.app_key
        data = OrderID + '#'
        data += ChannelID + "#"
        data += PayCode + "#"
        data += app_key
        digest = hashlib.md5(data.encode("utf-8")).hexdigest().upper()

        if digest != MD5Sign:
            return False

        return True

    @trace_service
    def process_charge_order(self, OrderID, ExData, CheckID, TradeID, Price, 
        ActionTime, ActionID, MSISDN, FeeMSISDN, AppID, ProgramID, PayCode, 
        TotalPrice, SubsNumb, SubsSeq, ChannelID, OrderType, OrderPayment, MD5Sign):
        if not self._check_sign(OrderID, ChannelID, PayCode, MD5Sign):
            return settings.MOBILE.code.invalid_md5
        if AppID != settings.MOBILE.app_id:
            return settings.MOBILE.code.invalid_app_id
        if OrderID == settings.MOBILE.fail_order:
            return settings.MOBILE.code.success

        charge_info = ujson.loads(ExData)
        user_id = int(charge_info['user_id'])
        item_id = int(charge_info['item_id'])
        if (item_id not in ITEMS.coins and item_id not in ITEMS.property_bags
            and item_id not in ITEMS.quick_coins and item_id not in ITEMS.same_items):
            return settings.MOBILE.code.no_item_id

        mobile_log = mobile_models.MobileLog.get_mobile_log(OrderID)
        if mobile_log is not None:
            return settings.MOBILE.code.success

        mobile_log = mobile_models.MobileLog()
        mobile_log.OrderID = OrderID
        mobile_log.item_id = item_id
        mobile_log.user_id = user_id
        mobile_log.CheckID = CheckID
        mobile_log.TradeID = TradeID
        mobile_log.Price = Price
        mobile_log.ActionTime = ActionTime
        mobile_log.ActionID = ActionID
        mobile_log.MSISDN = MSISDN
        mobile_log.FeeMSISDN = FeeMSISDN
        mobile_log.AppID = AppID
        mobile_log.ProgramID = ProgramID
        mobile_log.PayCode = PayCode
        mobile_log.TotalPrice = TotalPrice
        mobile_log.SubsNumb = SubsNumb
        mobile_log.SubsSeq = SubsSeq
        mobile_log.ChannelID = ChannelID
        mobile_log.OrderType = OrderType
        mobile_log.OrderPayment = OrderPayment
        mobile_log.MD5Sign = MD5Sign
        mobile_log.save()

        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        store_service = StoreService(self.service_repositories, self.activity_repository)
        store_service.charge(user_id, item_id, 1, player_extra.channel, 'charge', OrderID)
        
        if item_id in ITEMS.monthly_coins:
            now = int(time.time())
            player_extra.monthly_payment = True
            player_extra.monthly_pay_time = now
            player_extra.monthly_unsubscribe_time = 0
            player_extra.monthly_continuous = False
            player_extra.monthly_mature_end = False

            monthly_payment_expire = 60 * 60 * 24 * 30
            if player_extra.monthly_end_time <= now:
                player_extra.monthly_end_time = now + monthly_payment_expire
            else:
                player_extra.monthly_end_time += monthly_payment_expire

            player_models.PlayerExtra.update_player_extra(player_extra)

        charge_status = ChargeStatus()
        charge_status.charge(user_id, item_id)

        return settings.MOBILE.code.success
