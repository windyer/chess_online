import time
import hashlib
import urllib
import urlparse
import thread
import ujson
import requests

from django.conf import settings

import go.logging

from card.core.error.lobby.huawei_error import HuaweiError
from card.core.charge import ITEMS

from card.lobby.service.view_service import ViewService
from card.lobby.aop.logging import trace_service
from card.lobby.apps.store.service import StoreService
import card.lobby.apps.player.models as player_models
from card.lobby.apps.store.redis import ChargeStatus
from card.lobby.apps.player.service import PlayerService
from card.core.property.three import Property

from card.lobby.apps.huawei import models as huawei_models
from card.lobby.apps.huawei.crypto import CryptoHelper
from card.lobby.settings import player
from card.core.error.lobby.player_error import PlayerError

coin_items = set( ITEMS.coins.keys() ).union( set( ITEMS.quick_coins.keys() ) )

@go.logging.class_wrapper
class HuaweiService(ViewService):

    def __init__(self, service_repositories, activity_repository):
        super(HuaweiService, self).__init__(service_repositories, activity_repository)
        self.crypto = CryptoHelper()

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
            raise HuaweiError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        return item

    def _create_huawei_order(self, user_id, channel, item_id, item, orderid, app_id, privateKey, platpkey, notify_url):
        data = {}
        data['userName'] = ''
        data['userID'] = settings.HUAWEI.pay_id
        data['applicationID'] = app_id
        data['amount'] = float('%.2f' % item.price)
        data['productName'] = item.name



        req_text = ujson.dumps(data, ensure_ascii=False)
        req_sign = self.crypto.sign(req_text, privateKey)
        request_body={
            'transdata':req_text,
            'sign':req_sign,
            'signtype':'RSA'
        }
        create_order_url = settings.HUAWEI.create_huawei_order_url
        resp = None
        try:
            resp = requests.post(create_order_url, data=request_body, timeout=1)
        except Exception as ex:
            print ex, 'huawei line 81'
            raise HuaweiError.CREATE_ORDER_FAILED(user_id=user_id,
                    item_id=item_id, order_id=orderid, code=-1)
        text = resp.content
        reqData = urllib.unquote(str(text)).decode('utf8')
        decoded_data = urlparse.parse_qs(reqData)
        transdata = decoded_data["transdata"][0]
        transdata = ujson.loads(transdata)
        if "code" in transdata:
            raise HuaweiError.CREATE_ORDER_FAILED(user_id=user_id,
                item_id=item_id, order_id=orderid, code=transdata["code"])

        ok = self.crypto.segmentation_data(reqData, platpkey)
        if ok != True:
            raise HuaweiError.AUTH_HUAWEI_ORDER_FAILED(user_id=user_id,
                item_id=item_id, order_id=orderid)

        return transdata

    def _create_cp_order(self, user_id, item_id, item, channel_id, app_id):
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        order_id = "{0}_{1}_{2}_{3}".format(user_id, org_id, int(time.time() * 1000000), thread.get_ident())
        charge_log = huawei_models.HuaweiLog()
        charge_log.cporderid = order_id
        charge_log.appuserid = user_id
        charge_log.appid = app_id
        charge_log.waresid = settings.HUAWEI.huawei_items[item_id].pay_point_num
        charge_log.price = item.price
        charge_log.item_id = org_id
        charge_log.channel_id = channel_id
        charge_log.save()
        return order_id

    @trace_service
    def process_charge_order(self,data,requestId,sign):
        public_key = settings.HUAWEI.public_key
        ok = self.crypto.checksign(data,sign, public_key)
        if ok != True:
            raise HuaweiError.AUTH_HUAWEI_NOTIFY_ORDER_SIGN_FAILED(transid=requestId, sign=sign)

        transdata = data
        try:
            charge_log = huawei_models.HuaweiLog.get_huawei_log_by_cporderid(transdata["requestId"])
        except Exception:
            return '{"result":3}'

        if charge_log is None:
            self.logger.info("[transdata|%s] of [transid|%s] is not exists in database", transdata, transdata["requestId"])
            return '{"result":3}'

        if charge_log.result <= 0:
            self.logger.info("[transdata|%s] of [transid|%s] has been processed", transdata, transdata["requestId"])
            return '{"result":0}'

        item_id = int(charge_log.item_id)
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        user_id = charge_log.appuserid
        store_service = StoreService(self.service_repositories, self.activity_repository)
        store_service.charge(user_id, org_id, 1, charge_log.channel_id, 'charge', transdata["requestId"], revenue=int(float(transdata["amount"])))

        charge_status = ChargeStatus()
        charge_status.charge(user_id, item_id)
        charge_log.transid = transdata["orderId"]
        charge_log.money = float(transdata["amount"])
        charge_log.result = transdata["result"]
        charge_log.transtime = transdata["notifyTime"]
        charge_log.paytype = int (transdata["payType"])
        charge_log.save()
        try:
            player_charge = player_models.PlayerCharge.get_player_charge(user_id)
            money = player_charge.charge_money
            player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            player_charge.charge_money = money + int(float(transdata["amount"]))
            player_charge.save()
        except PlayerError.PLAYER_NOT_EXISTS:
            new_player_charge = player_models.PlayerCharge()
            new_player_charge.user_id = user_id
            new_player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            new_player_charge.charge_money = int(float(transdata["amount"]))
            new_player_charge.save()
        return '{"result":0}'

    @trace_service
    def create_charge_order(self, user_id, channel_id, item_id):
        app_id = settings.HUAWEI.app_id
        try:
            player_charge = player_models.PlayerCharge.get_player_charge(user_id)
            money = player_charge.charge_money
            date = player_charge.charge_times
            if date != time.strftime("%Y%m%d", time.localtime(time.time())):
                player_charge.charge_money = 0
                player_charge.save()
            if date == time.strftime("%Y%m%d", time.localtime(time.time())) and money >= player.PLAYER[
                'charge_limit'] and player.PLAYER['charge_limit']!=0:
                raise PlayerError.CHARGE_LIMIT(money=money)
                #return {'limit':0}
        except PlayerError.PLAYER_NOT_EXISTS:
            pass
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        if item_id not in settings.HUAWEI.huawei_items:
            raise HuaweiError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        item = self._get_purchase_item(user_id, item_id)

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        charge_status = ChargeStatus()
        if not charge_status.can_charge(user_id, profile.vip_title, item_id):
            raise HuaweiError.ITEM_HAS_CHARGED(user_id=user_id, item_id=item_id)
        order_id = self._create_cp_order(user_id, org_id, item, channel_id, app_id)
        data = {}
        data['userID'] = settings.HUAWEI.pay_id
        data['applicationID'] = app_id
        data['amount'] = str("%.2f"% item.price)
        data['productName'] = "buy_currency"
        data['requestId'] = order_id
        data['productDesc'] = item.name.encode('utf8')
        data['sign'] =self.crypto.sign(data,settings.HUAWEI.private_key)
        return data

