import time
import hashlib
import urllib
import  thread

from django.conf import settings

import go.logging

from card.core.error.lobby.skypay_error import SkypayError
from card.core.charge import ITEMS

from card.lobby.service.view_service import ViewService
from card.lobby.aop.logging import trace_service
from card.lobby.apps.store.service import StoreService
from card.lobby.apps.skypay import models as skypay_models
import card.lobby.apps.player.models as player_models
from card.lobby.apps.store.redis import ChargeStatus
from card.lobby.apps.skypay.redis import SkypayChargeStatus
from card.lobby.apps.player.service import PlayerService
from card.core.property.three import Property
from card.lobby.settings import player
from card.core.error.lobby.player_error import PlayerError

coin_items = set( ITEMS.coins.keys() ).union( set( ITEMS.quick_coins.keys() ) )

@go.logging.class_wrapper
class SkyPayService(ViewService):

    def _get_real_item_id(self, item_id, realAmount):
        assert realAmount > 0
        if item_id not in coin_items:
            return item_id

        #real_money = int(realAmount / 100)
        real_money = realAmount
        item = self._get_purchase_item(10000, item_id)
        price = item.price
        if real_money >= price:
            return item_id

        prices = settings.SKYPAY.check_items.keys()
        prices.sort()

        real_price = 0
        for p in prices:
            if p >= real_money:
                real_price = p
                break

        if real_price <= 0:
            real_price = 2
        return settings.SKYPAY.check_items[real_price].item_id

    def _process_order(self, orderId, cardType, skyId, resultCode, payNum, 
            realAmount, payTime, failure, failDesc, ext1, ext2, ext3, signMsg):
        item_id = int(ext1)
        user_id = int(ext2)
        count = int(ext3)

        try:
            charge_log = skypay_models.SkypayLog.get_skypay_log(orderId)
        except Exception:
            return "result={0}".format(1)
        
        if charge_log is None:
            self.logger.info("[order|%s] of [user|%s] is not exists in database", orderId, user_id)
            return "result={0}".format(1)
        if  int(charge_log.ext2) != user_id:
            self.logger.info("[order|%s] [user|%s] is inconsist with saved [user|%s]",
                            orderId, user_id, charge_log.ext2)
            return "result={0}".format(1)
        if charge_log.realAmount > 0:
            self.logger.info("[order|%s] of [user|%s] to buy [item_id|%s]"
                                " have been processed", orderId, user_id, item_id)
            return "result={0}".format(0)

        if item_id != int(charge_log.ext1):
            self.logger.warn("[order|%s] notified [item_id|%s] is not equal to saved [item_id|%s]",
                             orderId, item_id, charge_log.ext1)
        if realAmount > 0: 
            item_id = self._get_real_item_id(item_id, realAmount)
            player_extra = player_models.PlayerExtra.get_player_extra(user_id)
            store_service = StoreService(self.service_repositories, self.activity_repository)
            store_service.charge(user_id, item_id, 1, charge_log.channelId, 'charge', charge_log.orderId, revenue=realAmount/100)

            if item_id in ITEMS.monthly_coins:
                player_extra.monthly_payment = True
                player_extra.monthly_pay_time = int(time.time())
                player_extra.monthly_unsubscribe_time = 0
                player_extra.monthly_continuous = False
                player_extra.monthly_mature_end = False

                now = int(time.time())
                monthly_payment_expire = 60 * 60 * 24 * 30
                if player_extra.monthly_end_time <= now:
                    player_extra.monthly_end_time = now + monthly_payment_expire
                else:
                    player_extra.monthly_end_time += monthly_payment_expire

                player_models.PlayerExtra.update_player_extra(player_extra)

            charge_status = ChargeStatus()
            charge_status.charge(user_id, item_id)

            sms_items = settings.SKYPAY.sms_items
            if item_id in sms_items and settings.SKYPAY.sms_limtation.active:
                item = self._get_purchase_item(user_id, item_id)
                sky_charge_status = SkypayChargeStatus()
                sky_charge_status.charge(user_id, "sms", item)
        
        charge_log.ext1 = item_id
        charge_log.cardType = cardType
        charge_log.skyId = skyId
        charge_log.resultCode = resultCode
        charge_log.realAmount = realAmount
        charge_log.payTime = payTime
        charge_log.failure = failure
        charge_log.failDesc = failDesc
        charge_log.signMsg = signMsg
        charge_log.save()
        try:
            player_charge = player_models.PlayerCharge.get_player_charge(user_id)
            money = player_charge.charge_money
            player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            player_charge.charge_money = money + realAmount
            player_charge.save()
        except PlayerError.PLAYER_NOT_EXISTS:
            new_player_charge = player_models.PlayerCharge()
            new_player_charge.user_id = user_id
            new_player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            new_player_charge.charge_money = realAmount
            new_player_charge.save()
        return "result={0}".format(0)

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
            raise SkypayError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        return item

    def _create_charge_log(self, user_id, channel_id, item_id, item, pay_method, version_code, pay_type):
        order_id = "{0}_{1}_{2}_{3}".format(user_id, item_id, int(time.time() * 1000000), thread.get_ident())
        charge_log = skypay_models.SkypayLog()
        charge_log.orderId = order_id
        charge_log.skyId = 0
        charge_log.payMethod = pay_method
        charge_log.price = item.price * 100
        charge_log.systemId = settings.SKYPAY.system_id
        if not pay_type:
            pay_type = settings.SKYPAY.pay_type.charge
        charge_log.payType = pay_type
        charge_log.appVersion = version_code
        charge_log.channelId = channel_id
        charge_log.ext1 = item_id
        charge_log.ext2 = user_id
        charge_log.ext3 = 1
        charge_log.save()

        return charge_log

    def _get_order_sign(self, version_code, item, charge_log, pay_type):
        data = "merchantId=" + settings.SKYPAY.merchant_id
        data += "&appId=" + settings.SKYPAY.appid
        data += "&notifyAddress=" + urllib.quote(settings.SKYPAY.notify_address, 'utf-8')
        data += "&appName=" + settings.SKYPAY.app_name
        data += "&appVersion=" + str(version_code)
        if not pay_type:
            pay_type = settings.SKYPAY.pay_type.charge
        data += "&payType=" + str(pay_type)
        data += "&price=" + str(int(item.price * 100))
        data += "&orderId=" + charge_log.orderId
        if charge_log.ext1 is not None and charge_log.ext1 != "":
            data += "&reserved1=" + str(charge_log.ext1)
        if charge_log.ext2 is not None and charge_log.ext2 != "":
            data += "&reserved2=" + str(charge_log.ext2)
        if charge_log.ext3 is not None and charge_log.ext3 != "":
            data += "&reserved3=" + str(charge_log.ext3)
        data += "&key=" + settings.SKYPAY.secret_key
        return hashlib.md5(data.encode("utf-8")).hexdigest().upper()

    def _get_order_info(self, channel_id, pay_method, item_id, item, version_code, charge_log, pay_type, order_skipTip, order_skipResult):
        order_info = "notifyAddress=" + urllib.quote(settings.SKYPAY.notify_address, 'utf-8')
        order_info += "&merchantId=" + settings.SKYPAY.merchant_id
        order_info += "&appId=" + settings.SKYPAY.appid
        order_info += "&orderId=" + charge_log.orderId
        order_info += "&appName=" + settings.SKYPAY.app_name
        order_info += "&appVersion=" + str(version_code)
        order_info += "&price=" + str(int(item.price * 100))
        order_info += "&payMethod=" + pay_method
        order_info += "&gameType=" + settings.SKYPAY.game_type
        order_info += "&systemId=" + settings.SKYPAY.system_id
        if not pay_type:
            pay_type = settings.SKYPAY.pay_type.charge
        order_info += "&payType=" + str(pay_type)
        order_info += "&productName=" + item.name
        order_info += "&channelId=" + channel_id
        order_info += "&reserved1=" + ("" if charge_log.ext1 is None else str(charge_log.ext1))
        order_info += "&reserved2=" + ("" if charge_log.ext2 is None else str(charge_log.ext2))
        order_info += "&reserved3=" + ("" if charge_log.ext3 is None else str(charge_log.ext3))
        order_info += "&merchantSign=" + self._get_order_sign(version_code, item, charge_log, pay_type)
        if order_skipTip:
            order_info += "&order_skipTip=" + str(order_skipTip).lower()
        if order_skipResult:
            order_info += "&order_skipResult=" + str(order_skipResult).lower()
        
        if 'sms' == pay_method:
            #skypay_item = settings.SKYPAY.skypay_items[item_id]
            #pay_point_num = skypay_item.pay_point_num
            #order_desc = skypay_item.order_desc.format(item.price)
            item = self._get_purchase_item(0, item_id)
            order_desc = item.name
            #order_info = (order_info + "&payPointNum=" + str(pay_point_num)
            #                      + "&orderDesc=" + order_desc)
            order_info = (order_info + "&orderDesc=" + order_desc)
        
        return order_info

    def _get_order_info_new(self, channel_id, pay_method, item_id, item, version_code, charge_log, pay_type, order_skipTip,
                        order_skipResult):
        order_info = "notifyAddress=" + urllib.quote(settings.SKYPAY.notify_address, 'utf-8')
        order_info += "&merchantId=" + settings.SKYPAY.merchant_id
        order_info += "&appId=" + settings.SKYPAY.appid_new
        order_info += "&orderId=" + charge_log.orderId
        order_info += "&appName=" + settings.SKYPAY.app_name
        order_info += "&appVersion=" + str(version_code)
        order_info += "&price=" + str(int(item.price * 100))
        order_info += "&payMethod=" + pay_method
        order_info += "&gameType=" + settings.SKYPAY.game_type
        order_info += "&systemId=" + settings.SKYPAY.system_id
        if not pay_type:
            pay_type = settings.SKYPAY.pay_type.charge
        order_info += "&payType=" + str(pay_type)
        order_info += "&productName=" + item.name
        order_info += "&channelId=" + channel_id
        order_info += "&reserved1=" + ("" if charge_log.ext1 is None else str(charge_log.ext1))
        order_info += "&reserved2=" + ("" if charge_log.ext2 is None else str(charge_log.ext2))
        order_info += "&reserved3=" + ("" if charge_log.ext3 is None else str(charge_log.ext3))
        order_info += "&merchantSign=" + self._get_order_sign_new(version_code, item, charge_log, pay_type)
        if order_skipTip:
            order_info += "&order_skipTip=" + str(order_skipTip).lower()
        if order_skipResult:
            order_info += "&order_skipResult=" + str(order_skipResult).lower()

        if 'sms' == pay_method:
            # skypay_item = settings.SKYPAY.skypay_items[item_id]
            # pay_point_num = skypay_item.pay_point_num
            # order_desc = skypay_item.order_desc.format(item.price)
            item = self._get_purchase_item(0, item_id)
            order_desc = item.name
            # order_info = (order_info + "&payPointNum=" + str(pay_point_num)
            #                      + "&orderDesc=" + order_desc)
            order_info = (order_info + "&orderDesc=" + order_desc)

        return order_info
    def _get_order_sign_new(self, version_code, item, charge_log, pay_type):
        data = "merchantId=" + settings.SKYPAY.merchant_id
        data += "&appId=" + settings.SKYPAY.appid_new
        data += "&notifyAddress=" + urllib.quote(settings.SKYPAY.notify_address, 'utf-8')
        data += "&appName=" + settings.SKYPAY.app_name
        data += "&appVersion=" + str(version_code)
        if not pay_type:
            pay_type = settings.SKYPAY.pay_type.charge
        data += "&payType=" + str(pay_type)
        data += "&price=" + str(int(item.price * 100))
        data += "&orderId=" + charge_log.orderId
        if charge_log.ext1 is not None and charge_log.ext1 != "":
            data += "&reserved1=" + str(charge_log.ext1)
        if charge_log.ext2 is not None and charge_log.ext2 != "":
            data += "&reserved2=" + str(charge_log.ext2)
        if charge_log.ext3 is not None and charge_log.ext3 != "":
            data += "&reserved3=" + str(charge_log.ext3)
        data += "&key=" + settings.SKYPAY.secret_key
        return hashlib.md5(data.encode("utf-8")).hexdigest().upper()

    @trace_service
    def process_charge_order(self, orderId, cardType, skyId, resultCode, payNum, 
            realAmount, payTime, failure, failDesc, ext1, ext2, ext3, signMsg, query_string):
        sign_source = query_string[0:query_string.find("&signMsg=")]
        sign_source += "&key=" + settings.SKYPAY.secret_key

        digest = hashlib.md5(sign_source.encode("utf-8"))
        if digest.hexdigest().upper() != signMsg:
            return "result={0}".format(1)

        return self._process_order(orderId, cardType, skyId, resultCode, payNum, 
                    realAmount, payTime, failure, failDesc, ext1, ext2, ext3, signMsg)

    @trace_service
    def create_charge_order(self, user_id, channel_id, item_id, version_code, non_sms, pay_type, order_skipTip=None, order_skipResult=None, skypay_method=None):
        try:
            player_charge = player_models.PlayerCharge.get_player_charge(user_id)
            money = player_charge.charge_money
            date= player_charge.charge_times
            if date != time.strftime("%Y%m%d", time.localtime(time.time())):
                player_charge.charge_money = 0
                player_charge.save()
            if date == time.strftime("%Y%m%d", time.localtime(time.time())) and money >= player.PLAYER[
                'charge_limit']and player.PLAYER['charge_limit']!=0:
                raise PlayerError.CHARGE_LIMIT(money=money)
        except PlayerError.PLAYER_NOT_EXISTS:
            pass
        item = self._get_purchase_item(user_id, item_id)
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id

        assert item_id in settings.SKYPAY.sms_items or item_id in settings.SKYPAY.alipay_items
        
        if channel_id in settings.SKYPAY.charge_types:
            sms_items = settings.SKYPAY.charge_types[channel_id].sms_items
            alipay_items = settings.SKYPAY.charge_types[channel_id].alipay_items
        else:
            sms_items = settings.SKYPAY.sms_items
            alipay_items = settings.SKYPAY.alipay_items
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        if int(player_extra.app_version.replace('.','')) >= 200:
            pay_method = 'sms'
            if non_sms:
                pay_method = '3rd'
        else:
            if item_id in sms_items:
                pay_method = 'sms'
            elif item_id in alipay_items:
                pay_method = '3rd'
            pay_method = '3rd'

        #if item_id == Property.NEWBIE_COIN_BAG_ONE.item_id:
        #    pay_method = 'sms'
        if pay_method == 'sms' and settings.SKYPAY.sms_limtation.active:
            sky_charge_status = SkypayChargeStatus()
            status = sky_charge_status.sms_status(user_id)
            device_status = status["device"]
            player_status = status["user"]
            if device_status["daily_sms_money"] >= settings.SKYPAY.sms_limtation.daily_device:
                raise SkypayError.MAX_SMS_CHARGE_LIMITATION(user_id=user_id)
            if player_status["daily_sms_money"] >= settings.SKYPAY.sms_limtation.daily_user:
                raise SkypayError.MAX_SMS_CHARGE_LIMITATION(user_id=user_id)
            if device_status["month_sms_money"] >= settings.SKYPAY.sms_limtation.month_device:
                raise SkypayError.MAX_SMS_CHARGE_LIMITATION(user_id=user_id)
            if player_status["month_sms_money"] >= settings.SKYPAY.sms_limtation.month_user:
                raise SkypayError.MAX_SMS_CHARGE_LIMITATION(user_id=user_id)

        if skypay_method:
            pay_method = skypay_method
        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        charge_status = ChargeStatus()
        if not charge_status.can_charge(user_id, profile.vip_title, item_id):
            raise SkypayError.ITEM_HAS_CHARGED(user_id=user_id, item_id=item_id)
            
        charge_log = self._create_charge_log(user_id, channel_id, org_id, item, pay_method, version_code, pay_type)
        if settings.SKYPAY.appid_new in channel_id:
            order_info = self._get_order_info_new(channel_id, pay_method, item_id, item, version_code, charge_log, pay_type,
                                              order_skipTip, order_skipResult)
        else:
            order_info = self._get_order_info(channel_id, pay_method, item_id, item, version_code, charge_log, pay_type, order_skipTip, order_skipResult)


        return {'order_info':order_info, 'order_id':charge_log.orderId}
