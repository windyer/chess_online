import time
import hashlib
import urllib
import urlparse
import thread
import ujson
import requests

from django.conf import settings

import go.logging

from card.core.error.lobby.iapppay_error import IApppayError
from card.core.charge import ITEMS

from card.lobby.service.view_service import ViewService
from card.lobby.aop.logging import trace_service
from card.lobby.apps.store.service import StoreService
import card.lobby.apps.player.models as player_models
from card.lobby.apps.store.redis import ChargeStatus
from card.lobby.apps.player.service import PlayerService
from card.core.property.three import Property

from card.lobby.apps.iapppay import models as iapppay_models
from card.lobby.apps.iapppay.crypto import CryptoHelper
from card.lobby.settings import player
from card.core.error.lobby.player_error import PlayerError

coin_items = set( ITEMS.coins.keys() ).union( set( ITEMS.quick_coins.keys() ) )

@go.logging.class_wrapper
class IAppPayService(ViewService):

    def __init__(self, service_repositories, activity_repository):
        super(IAppPayService, self).__init__(service_repositories, activity_repository)
        self.crypto = CryptoHelper()
        self.privateKeys = {}
        self.platpkeys = {}

        for app_id in settings.IAPPPAY.app_conf:
            self.privateKeys[app_id] = CryptoHelper.importKey(settings.IAPPPAY.app_conf[app_id].appvkey)
            self.platpkeys[app_id] = CryptoHelper.importKey(settings.IAPPPAY.app_conf[app_id].platpkey)

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
            raise IApppayError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        return item

    def _create_iappay_order(self, user_id, channel, item_id, item, orderid, app_id, privateKey, platpkey, notify_url):
        data = {}
        data['appid'] = app_id
        data['waresid'] = settings.IAPPPAY.iapppay_items[item_id].pay_point_num
        data['cporderid'] = orderid
        data['price'] = item.price
        #if channel in ['lenovo_duowan',]:
        #    data['price'] = int(data['price'] / 0.7) + 1
        data['currency'] = "RMB"
        data['appuserid'] = str(user_id)
        data['cpprivateinfo'] = "reserved"
        data['notifyurl'] = notify_url

        req_text = ujson.dumps(data, ensure_ascii=False)
        req_sign = self.crypto.sign(req_text, privateKey)  
        request_body={
            'transdata':req_text,
            'sign':req_sign,
            'signtype':'RSA'
        }
        create_order_url = settings.IAPPPAY.create_iapppay_order_url
        resp = None
        try:
            resp = requests.post(create_order_url, data=request_body, timeout=1)
        except Exception as ex:
            print ex, 'iapppay line 81'
            raise IApppayError.CREATE_ORDER_FAILED(user_id=user_id, 
                    item_id=item_id, order_id=orderid, code=-1)
        text = resp.content
        reqData = urllib.unquote(str(text)).decode('utf8')
        decoded_data = urlparse.parse_qs(reqData)
        transdata = decoded_data["transdata"][0]
        transdata = ujson.loads(transdata)
        if "code" in transdata:
            raise IApppayError.CREATE_ORDER_FAILED(user_id=user_id, 
                item_id=item_id, order_id=orderid, code=transdata["code"])

        ok = self.crypto.segmentation_data(reqData, platpkey)
        if ok != True:
            raise IApppayError.AUTH_IAPPPAY_ORDER_FAILED(user_id=user_id, 
                item_id=item_id, order_id=orderid)

        return transdata

    def _create_cp_order(self, user_id, item_id, item, channel_id, app_id):
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        order_id = "{0}_{1}_{2}_{3}".format(user_id, org_id, int(time.time() * 1000000), thread.get_ident())
        charge_log = iapppay_models.IApppayLog()
        charge_log.cporderid = order_id
        charge_log.appuserid = user_id
        charge_log.appid = app_id
        charge_log.waresid = settings.IAPPPAY.iapppay_items[item_id].pay_point_num
        charge_log.price = item.price
        charge_log.item_id = org_id
        charge_log.channel_id = channel_id
        charge_log.save()

        return charge_log

    @trace_service
    def process_charge_order(self, request_body, transdata, sign, signtype, app_id):
        if not app_id in self.platpkeys:
            raise IApppayError.AUTH_IAPPPAY_NOTIFY_ORDER_FAILED(transdata=transdata, sign=sign)

        platpkey = self.platpkeys[app_id]
        ok = self.crypto.checksign(transdata, sign, platpkey)
        if ok != True:
            raise IApppayError.AUTH_IAPPPAY_NOTIFY_ORDER_FAILED(transdata=transdata, sign=sign)

        transdata = ujson.loads(transdata)
        try:
            charge_log = iapppay_models.IApppayLog.get_iapppay_log_by_transid(transdata["transid"])
        except Exception:
            return "FAILURE"

        if charge_log is None:
            self.logger.info("[transdata|%s] of [transid|%s] is not exists in database", transdata, transdata["transid"])
            return "FAILURE"

        if charge_log.result <= 0:
            self.logger.info("[transdata|%s] of [transid|%s] has been processed", transdata, transdata["transid"])
            return "SUCCESS"

        item_id = int(charge_log.item_id)
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        user_id = charge_log.appuserid

        item = self._get_purchase_item(user_id, item_id)
        #if item.price > transdata['money']:
        #    self.logger.info("[transdata|%s] of [transid|%s] [item|%d] [price|%d] [pay|%d]", transdata, transdata["transid"],
        #        item_id, item.price, transdata['money'])
        #    return "FAILURE"
        
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        store_service = StoreService(self.service_repositories, self.activity_repository)
        store_service.charge(user_id, org_id, 1, charge_log.channel_id, 'charge', transdata["transid"], revenue=int(transdata["money"]))

        charge_status = ChargeStatus()
        charge_status.charge(user_id, item_id)
        charge_log.transtype = transdata["transtype"]
        charge_log.feetype = transdata["feetype"]
        charge_log.money = transdata["money"]
        charge_log.currency = transdata["currency"]
        charge_log.result = transdata["result"]
        charge_log.transtime = transdata["transtime"]
        charge_log.cpprivate = transdata["cpprivate"]
        charge_log.paytype = transdata["paytype"]
        charge_log.save()
        try:
            player_charge = player_models.PlayerCharge.get_player_charge(user_id)
            money = player_charge.charge_money
            player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            player_charge.charge_money = money + transdata["money"]
            player_charge.save()
        except PlayerError.PLAYER_NOT_EXISTS:
            new_player_charge = player_models.PlayerCharge()
            new_player_charge.user_id = user_id
            new_player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            new_player_charge.charge_money = transdata["money"]
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
                'charge_limit'] and player.PLAYER['charge_limit']!=0:
                raise PlayerError.CHARGE_LIMIT(money=money)
                #return {'limit':0}
        except PlayerError.PLAYER_NOT_EXISTS:
            pass
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        if item_id not in settings.IAPPPAY.iapppay_items:
            raise IApppayError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        item = self._get_purchase_item(user_id, item_id)

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        charge_status = ChargeStatus()
        if not charge_status.can_charge(user_id, profile.vip_title, item_id):
            raise IApppayError.ITEM_HAS_CHARGED(user_id=user_id, item_id=item_id)

        if not app_id in self.privateKeys or not app_id in self.platpkeys:
            raise IApppayError.APP_ID_INVALIDE(app_id=app_id)

        privateKey = self.privateKeys[app_id]
        platpkey = self.platpkeys[app_id]
        notify_url = settings.IAPPPAY.app_conf[app_id].notify_url

        charge_log = self._create_cp_order(user_id, org_id, item, channel_id, app_id)
        resp = self._create_iappay_order(user_id, channel_id, item_id, item, charge_log.cporderid, app_id, privateKey, platpkey, notify_url)
        charge_log.transid = resp["transid"]
        charge_log.save()
        return {'transid':resp["transid"]}

    @trace_service
    def create_normal_charge_order(self, user_id, app_id, channel_id, item_id):
        return self.create_charge_order(user_id, channel_id, item_id, app_id)

    @trace_service
    def process_normal_charge_order(self, request_body, app_id, transdata, sign, signtype):
        return self.process_charge_order(request_body, transdata, sign, signtype, app_id)
