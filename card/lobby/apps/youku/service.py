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

from card.core.error.lobby.youku_error import YoukuError
from card.core.charge import ITEMS

from card.lobby.service.view_service import ViewService
from card.lobby.aop.logging import trace_service
from card.lobby.apps.store.service import StoreService
import card.lobby.apps.player.models as player_models
from card.lobby.apps.store.redis import ChargeStatus
from card.lobby.apps.player.service import PlayerService
from card.core.property.three import Property

from card.lobby.apps.youku import models as youku_models
from card.core.error.lobby.player_error import PlayerError
from card.lobby.settings import player



@go.logging.class_wrapper
class YoukuService(ViewService):

    def __init__(self, service_repositories, activity_repository):
        super(YoukuService, self).__init__(service_repositories, activity_repository)

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
            raise YoukuError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        return item

    def _create_cp_order(self, user_id, item_id, item, channel_id, app_id):
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        #md = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()
        order_id = "{0}_{1}_{2}_{3}".format(user_id, org_id, int(time.time() * 1000000), thread.get_ident())
        charge_log = youku_models.YoukuLog()
        charge_log.cporderid = order_id
        charge_log.appuserid = user_id
        charge_log.appid = app_id
        charge_log.waresid = settings.YOUKU.youku_items[item_id].pay_point_num
        charge_log.price = item.price
        charge_log.item_id = org_id
        charge_log.channel_id = channel_id
        charge_log.save()

        return charge_log

    def check_charge_order(self, transid):
        order_type = "1"
        app_id = settings.YOUKU.app_id
        secret_key = settings.YOUKU.secret_key
        sign = hashlib.md5(app_id + transid + secret_key).hexdigest()
        action = "10002"
        request_body={
            'AppID':app_id,
            'CooperatorOrderSerial':transid,
            'Sign':sign,
            'OrderType':order_type,
            'Action':action,
        }
        query_url = settings.YOUKU.query_order_url
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
    def process_charge_order(self, orderid,amount, passthrough, sign,uid):

        callbackurl=settings.YOUKU.notify_url
        pay_key=settings.YOUKU.PayKey
        if uid == '':
            massege='{0}?apporderID={1}&price={2}'.format(callbackurl,orderid,amount)
        else:
            massege='{0}?apporderID={1}&price={2}&uid={3}'.format(callbackurl,orderid,amount,uid)
        s_sign = hmac.new(pay_key, massege, hashlib.md5).hexdigest()
        if sign != s_sign:
            self.logger.debug(
                '[youku_charge] [orderid|%s] [amount|%s]  [sign|%s] [s_sign|%s]  not match',
                orderid, amount,  sign, s_sign)
            return {'status':'failed', 'desc':'sign wrong'}

        #if status != 'success':
            #self.logger.debug('[youku_charge] [orderid|%s] [amount|%s] [status|%s] [id|%s] failed',
            #                  orderid, amount, status, cpdefinepart)
            #return 'FAILED'
        '''
        try:
            _id = int(orderid.strip())
            charge_log = youku_models.YoukuLog.get_by_id(_id)
            if charge_log.result == 1:
                self.logger.info("[orderid|%s]  has been processed", orderid)
                return {'status':'success', 'desc':'success'}
        except Exception:
            self.logger.debug('[youku_charge] [orderid|%s] [amount|%s]  failed',
                              orderid, amount)
            return {'status':'failed', 'desc':'order wromg'}
        '''
        try:
            charge_log = youku_models.YoukuLog.get_youku_log_by_transid(orderid)
            if charge_log.result == 1:
                self.logger.debug(
                    '[youku_charge] [orderid|%s] [amount|%s]  [other_id|%s] already exist',
                    orderid, amount, charge_log.id)
                return {'status':'failed', 'desc':'order already exist'}
        except Exception:
            return {'status': 'failed', 'desc': 'order wromg'}

        if charge_log is None:
            self.logger.info("[orderid|%s]  is not exists in database", orderid)
            return {'status':'failed', 'desc':'no order'}

        item_id = int(charge_log.item_id)
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        user_id = int(charge_log.appuserid)
        item = self._get_purchase_item(user_id, item_id)
        youku_amount = int(amount.strip())
        if item is None or item.price * 100 > youku_amount:
            self.logger.debug('[orderid|%s] [amount|%s] [price|%d] not match',
                              orderid, amount, item.price * 100)
            return {'status':'failed', 'desc':'order wrong'}
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        store_service = StoreService(self.service_repositories, self.activity_repository)
        store_service.charge(user_id, org_id, 1, charge_log.channel_id, 'charge', orderid,
                             revenue=int(youku_amount / 100))

        charge_status = ChargeStatus()
        charge_status.charge(user_id, item_id)

        charge_log.money = youku_amount
        charge_log.result = 1
        charge_log.transtime = int(time.time())
        charge_log.transid = orderid
        charge_log.save()
        try:
            player_charge = player_models.PlayerCharge.get_player_charge(user_id)
            money = player_charge.charge_money
            player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            player_charge.charge_money = money + youku_amount
            player_charge.save()
        except PlayerError.PLAYER_NOT_EXISTS:
            new_player_charge = player_models.PlayerCharge()
            new_player_charge.user_id = user_id
            new_player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            new_player_charge.charge_money = youku_amount
            new_player_charge.save()
        return {'status':'success', 'desc':'success'}
    '''
    @trace_service
    def process_charge_order(self, appid, orderid, amount, unit, jfd, status, paychannel, sign, cpdefinepart):
        s_sign = hashlib.md5(str(settings.YOUKU.app_id) + orderid + amount + unit + \
                status + paychannel + settings.YOUKU.secret_key).hexdigest()
        if sign != s_sign:
            self.logger.debug('[youku_charge] [orderid|%s] [amount|%s] [status|%s] [sign|%s] [s_sign|%s] [id|%s] not match',
                orderid, amount, status, sign, s_sign, cpdefinepart)
            return 'FAILED'

        if status != 'success':
            self.logger.debug('[youku_charge] [orderid|%s] [amount|%s] [status|%s] [id|%s] failed',
                orderid, amount, status, cpdefinepart)
            return 'FAILED'
        try:
            _id = int(cpdefinepart.strip())
            charge_log = youku_models.YoukuLog.get_by_id(_id)
            if charge_log.result == 1:
                self.logger.info("[orderid|%s] [id|%s] has been processed", orderid, cpdefinepart)
                return 'SUCCESS'
        except Exception:
            self.logger.debug('[youku_charge] [orderid|%s] [amount|%s] [status|%s] [id|%s] failed',
                orderid, amount, status, cpdefinepart)
            return 'FAILED'

        try:
            old_log = youku_models.YoukuLog.get_youku_log_by_transid(orderid)
            if old_log != None:
                self.logger.debug('[youku_charge] [orderid|%s] [amount|%s] [status|%s] [id|%s] [other_id|%s] already exist',
                    orderid, amount, status, cpdefinepart, charge_log.id)
                return 'FAILED'
        except Exception:
            pass

        if charge_log is None:
            self.logger.info("[orderid|%s] [id|%s] is not exists in database", orderid, cpdefinepart)
            return 'FAILED'

        item_id = int(charge_log.item_id)
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        user_id = int(charge_log.appuserid)
        item = self._get_purchase_item(user_id, item_id)
        youku_amount = int(amount.strip())
        if item is None or item.price * 100 > youku_amount:
            self.logger.debug('[orderid|%s] [id|%s] [amount|%s] [price|%d] not match',
                orderid, cpdefinepart, amount, item.price * 100)
            return 'FAILED'
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        store_service = StoreService(self.service_repositories, self.activity_repository)
        store_service.charge(user_id, org_id, 1, charge_log.channel_id, 'charge', orderid, revenue=int(youku_amount/100))

        charge_status = ChargeStatus()
        charge_status.charge(user_id, item_id)

        charge_log.money = youku_amount
        charge_log.result = 1
        charge_log.transtime = int(time.time())
        charge_log.transid = orderid
        charge_log.save()
        return 'SUCCESS'
        '''

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
        if item_id not in settings.YOUKU.youku_items:
            raise YoukuError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        item = self._get_purchase_item(user_id, item_id)

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        charge_status = ChargeStatus()
        if not charge_status.can_charge(user_id, profile.vip_title, item_id):
            raise YoukuError.ITEM_HAS_CHARGED(user_id=user_id, item_id=item_id)

        app_id = settings.YOUKU.app_id
        charge_log = self._create_cp_order(user_id, org_id, item, channel_id, app_id)
        charge_log.transid = charge_log.cporderid
        charge_log.save()

        return {'transid':charge_log.transid,'callbackurl':settings.YOUKU.notify_url,'pay_point':settings.YOUKU.youku_items[item_id].pay_point_num, 'item_id':item_id, 'price':item.price, 'name':item.name}
