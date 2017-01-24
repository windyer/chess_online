import time
import urllib
import urlparse
import thread
import ujson
import requests
from go.containers import redis

from django.conf import settings

import go.logging

from card.core.error.lobby.coolpad_error import CoolpadError
from card.core.charge import ITEMS

from card.lobby.service.view_service import ViewService
from card.lobby.aop.logging import trace_service
from card.lobby.apps.store.service import StoreService
import card.lobby.apps.player.models as player_models
from card.lobby.apps.store.redis import ChargeStatus
from card.lobby.apps.player.service import PlayerService

from card.lobby.apps.coolpad import models as coolpad_models
from card.lobby.apps.coolpad.crypto import CryptoHelper
from card.lobby.settings import player
from card.core.error.lobby.player_error import PlayerError

coin_items = set( ITEMS.coins.keys() ).union( set( ITEMS.quick_coins.keys() ) )

@go.logging.class_wrapper
class CoolpadService(ViewService):

    def __init__(self, service_repositories, activity_repository):
        super(CoolpadService, self).__init__(service_repositories, activity_repository)
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
            raise CoolpadError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        return item

    def _create_coolpad_order(self, user_id, item_id, item, orderid, app_id, privateKey, platpkey, notify_url):
        data = {}
        data['appid'] = app_id
        data['waresid'] = settings.COOLPAD.coolpad_items[item_id].pay_point_num
        data['cporderid'] = orderid
        data['price'] = item.price
        data['currency'] = "RMB"
        data['appuserid'] = str(user_id)
        data['notifyurl'] = notify_url

        req_text = ujson.dumps(data, ensure_ascii=False)
        privateKey=CryptoHelper.importKey(privateKey)
        platpkey = CryptoHelper.importKey(platpkey)
        req_sign = self.crypto.sign(req_text, privateKey)
        request_body={
            'transdata':req_text,
            'sign':req_sign,
            'signtype':'RSA'
        }
        create_order_url = settings.COOLPAD.query_order_url
        resp = requests.get(create_order_url, data=request_body, timeout=0.1)
        text = resp.content
        reqData = urllib.unquote(str(text)).decode('utf8')
        decoded_data = urlparse.parse_qs(reqData)

        transdata = decoded_data["transdata"][0]
        transdata = ujson.loads(transdata)
        if "code" in transdata:
            raise CoolpadError.CREATE_ORDER_FAILED(user_id=user_id,
                item_id=item_id, order_id=orderid, code=transdata["code"])

        ok = self.crypto.segmentation_data(reqData, platpkey)
        if ok != True:
            raise CoolpadError.AUTH_COOLPAD_ORDER_FAILED(user_id=user_id,
                item_id=item_id, order_id=orderid)

        return transdata

    def _create_cp_order(self, user_id, item_id, item, channel_id, app_id):
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        order_id = "{0}_{1}_{2}_{3}".format(user_id, org_id, int(time.time() * 1000000), thread.get_ident())
        charge_log = coolpad_models.CoolpadLog()
        charge_log.cporderid = order_id
        charge_log.appuserid = user_id
        charge_log.appid = app_id
        charge_log.waresid = settings.COOLPAD.coolpad_items[item_id].pay_point_num
        charge_log.price = item.price
        charge_log.item_id = org_id
        charge_log.channel_id = channel_id
        charge_log.save()

        return charge_log

    @trace_service
    def process_charge_order(self,transdata, sign, signtype):
        platpkey = settings.COOLPAD.pubkey
        platpkey = CryptoHelper.importKey(platpkey)
        ok = self.crypto.checksign(transdata, sign, platpkey)
        if ok != True:
            raise CoolpadError.AUTH_COOLPADF_NOTIFY_ORDER_FAILED(transdata=transdata, sign=sign)

        transdata = ujson.loads(transdata)
        try:
            charge_log = coolpad_models.CoolpadLog.get_coolpad_log_by_transid(transdata["transid"])
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
    def create_charge_order(self, user_id, channel_id, item_id):
        try:
            app_id = settings.COOLPAD.app_id
            player_charge = player_models.PlayerCharge.get_player_charge(user_id)
            money = player_charge.charge_money
            date = player_charge.charge_times
            if date != time.strftime("%Y%m%d", time.localtime(time.time())):
                player_charge.charge_money = 0
                player_charge.save()
            if date == time.strftime("%Y%m%d", time.localtime(time.time())) and money >= player.PLAYER[
                'charge_limit'] and player.PLAYER['charge_limit']!=0:
                raise PlayerError.CHARGE_LIMIT(money=money)
        except PlayerError.PLAYER_NOT_EXISTS:
            pass
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        if item_id not in settings.COOLPAD.coolpad_items:
            raise CoolpadError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        item = self._get_purchase_item(user_id, item_id)

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        charge_status = ChargeStatus()
        if not charge_status.can_charge(user_id, profile.vip_title, item_id):
            raise CoolpadError.ITEM_HAS_CHARGED(user_id=user_id, item_id=item_id)
        privateKey = settings.COOLPAD.prvkey
        platpkey = settings.COOLPAD.pubkey
        notify_url = settings.COOLPAD.notify_url
        re = redis.Redis(**settings.PERSIST_REDIS)
        coolpad_token=re.get(user_id)
        coolpad_token=ujson.loads(coolpad_token)
        token = coolpad_token['access_token']
        openid = coolpad_token['openid']
        charge_log = self._create_cp_order(user_id, org_id, item, channel_id, app_id)
        resp = self._create_coolpad_order(user_id, item_id, item, charge_log.cporderid, app_id, privateKey, platpkey, notify_url)
        charge_log.transid = resp["transid"]
        charge_log.save()

        return {'transid':resp["transid"],'authToken':token,'openID':openid}

    @trace_service
    def create_normal_charge_order(self, user_id, app_id, channel_id, item_id):
        return self.create_charge_order(user_id, channel_id, item_id, app_id)

    @trace_service
    def process_normal_charge_order(self, request_body, app_id, transdata, sign, signtype):
        return self.process_charge_order(request_body, transdata, sign, signtype, app_id)
