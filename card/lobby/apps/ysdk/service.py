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

from django.conf import settings

import go.logging

from card.core.error.lobby import YsdkError,PlayerError
from card.core.charge import ITEMS

from card.lobby.service.view_service import ViewService
from card.lobby.aop.logging import trace_service
from card.lobby.apps.store.service import StoreService
import card.lobby.apps.player.models as player_models
from card.lobby.apps.store.redis import ChargeStatus
from card.lobby.apps.player.service import PlayerService
from card.core.property.three import Property

from card.lobby.apps.ysdk import models as ysdk_models
import makesig
@go.logging.class_wrapper
class YsdkService(ViewService):

    def __init__(self, service_repositories, activity_repository):
        super(YsdkService, self).__init__(service_repositories, activity_repository)

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
            raise YsdkError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        return item

    def _create_cp_order(self, user_id, item_id, item, channel_id, app_id):
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        md = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()
        order_id = "{0}_{1}_{2}_{3}".format(user_id, org_id, int(time.time() * 1000000), thread.get_ident())
        charge_log = ysdk_models.YsdkLog()
        charge_log.cporderid = order_id
        charge_log.appuserid = user_id
        charge_log.appid = app_id
        charge_log.waresid = settings.YSDK.ysdk_items[item_id].pay_point_num
        charge_log.price = item.price
        charge_log.item_id = org_id
        charge_log.channel_id = channel_id
        #charge_log.save()

        return charge_log,order_id

    def check_charge_order(self, transid):
        order_type = "1"
        app_id = settings.YSDK.app_id
        secret_key = settings.YSDK.secret_key
        sign = hashlib.md5(app_id + transid + secret_key).hexdigest()
        action = "10002"
        request_body={
            'AppID':app_id,
            'CooperatorOrderSerial':transid,
            'Sign':sign,
            'OrderType':order_type,
            'Action':action,
        }
        query_url = settings.YSDK.query_order_url
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
    def process_charge_order(self,url_path,params):

        appid=params['appid']
        sig=params['sig']
        amount=params['amt']
        taken=params['token']
        app_key=settings.YSDK.qq_app_key
        if appid == settings.YSDK.wx_app_id:
            app_key = settings.YSDK.wx_app_key
        if makesig.verify_pay_callback_sig(app_key,'get',url_path,params)==0:
            self.logger.debug('[sign|%s] not match',sig)
            return json.dumps({"ret":4,"msg":"failed:(sig)"})

        try:

            charge_log = ysdk_models.YsdkLog.get_by_takenid(taken)
            orderid=charge_log.cporderid
            if charge_log.result == 1:
                self.logger.info("[orderid|%s]  has been processed", orderid)
                return json.dumps({"ret":0,"msg":"OK"})
        except Exception:
            self.logger.debug('[ysdk_charge] [orderid|%s] [amount|%s] failed',orderid, amount)
            return json.dumps({"ret":4,"msg":"failed"})

        try:
            old_log = ysdk_models.YsdkLog.get_ysdk_log_by_transid(orderid)
            if old_log != None:
                self.logger.debug('[ysdk_charge] [orderid|%s] [amount|%s] [other_id|%s] already exist',
                    orderid, amount, charge_log.id)
                return json.dumps({"ret":4,"msg":"failed"})
        except Exception:
            pass

        if charge_log is None:
            self.logger.info("[orderid|%s]  is not exists in database", orderid)
            return json.dumps({"ret":4,"msg":"failed"})


        item_id = int(charge_log.item_id)
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        user_id = int(charge_log.appuserid)
        item = self._get_purchase_item(user_id, item_id)
        ysdk_amount = int(amount.strip())
        if item is None or item.price * 10 > ysdk_amount:
            self.logger.debug('[orderid|%s] [amount|%s] [price|%d] not match',
                orderid,  amount, item.price * 10)
            return json.dumps({"ret":4,"msg":"failed"})
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        store_service = StoreService(self.service_repositories, self.activity_repository)
        store_service.charge(user_id, org_id, 1, charge_log.channel_id, 'charge', orderid, revenue=int(ysdk_amount/10))

        charge_status = ChargeStatus()
        charge_status.charge(user_id, item_id)

        charge_log.money = ysdk_amount
        charge_log.result = 1
        charge_log.transtime = int(time.time())
        charge_log.transid = orderid
        charge_log.save()
        return json.dumps({"ret":0,"msg":"OK"})

    def _create_ysdk_order(self,account_type, app_id, app_key, open_id, open_key, pf, pfkey, zoneid, item, count):
        ts = int(time.time())
        payitem = '{0}*{1}*{2}'.format(item.item_id, item.price*10, count)
        des = item.name
        goodsurl = settings.YSDK.default_goods_url
        if item.item_id in settings.YSDK.ysdk_items:
            des = settings.YSDK.ysdk_items[item.item_id].order_desc
            goodsurl = settings.YSDK.ysdk_items[item.item_id].url

        amt = item.price * count
        session_id = settings.YSDK.qq_session_id
        session_type = settings.YSDK.qq_session_type
        if account_type =='2':
            session_id=settings.YSDK.wx_session_id
            session_type = settings.YSDK.wx_session_type
        cookies = dict(session_id=session_id,session_type=session_type,org_loc=settings.YSDK.org_loc)
        params={
            'openid':str(open_id),
            'openkey':str(open_key),
            'appid':app_id,
            'ts':str(ts),
            'payitem':payitem,
            'goodsmeta':u's*s',
            'goodsurl':goodsurl,
            'pf':pf,
            'pfkey':pfkey,
            'zoneid':str(zoneid),
            'appmode':'1',
            'amt':str(amt),
        }

        url_path=settings.YSDK.url_path
        sig=makesig.mksig(app_key,'get',url_path,params)
        str_params = makesig.make_str_params(params)
        order_url = settings.YSDK.order_url
        order_url = '{0}?{1}&sig={2}'.format(order_url,str_params,sig)
        resp = requests.get(url=order_url,cookies=cookies)
        self.logger.debug('resp|%s',str(resp.content))
        if resp is None or resp.content is None or resp.content == '':
            return False, -1
        js = json.loads(resp.content.decode('string-escape').strip('"'))
        code = js['ret']
        if code != 0:
            return False, code
        return True, js['url_params'],js['token']

    #@trace_service
    #def create_charge_order(self, user_id,open_id, open_key, pf, pf_key, #channel_id, item_id):
    #
    #    org_id = item_id
    #    if item_id in ITEMS.same_items:
    #        item_id = ITEMS.same_items[item_id].item_id
    #    if item_id not in settings.YSDK.ysdk_items:
    #        raise YsdkError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
    #    item = self._get_purchase_item(user_id, item_id)
#
    #    player_service = PlayerService(self.service_repositories, self.#activity_repository)
    #    profile = player_service.get_profile(user_id)
    #    charge_status = ChargeStatus()
    #    if not charge_status.can_charge(user_id, profile.vip_title, item_id):
    #        raise YsdkError.ITEM_HAS_CHARGED(user_id=user_id, item_id=item_id)
#
    #    try:
    #        ysdk = ysdk_models.Ysdk.get_ysdk_by_user_id(user_id=user_id)
    #    except YsdkError.USER_ID_NOT_EXIST:
    #        raise YsdkError.USER_ID_NOT_EXIST(user_id=user_id)
    #    app_id = settings.YSDK.qq_app_id
    #    app_key = settings.YSDK.order_key
    #    if ysdk.account_type == '2':
    #        app_id = settings.YSDK.wx_app_id
    #        app_key = settings.YSDK.order_key
#
    #    player_extra = player_models.PlayerExtra.get_player_extra(user_id)
    #    charge_log = self._create_cp_order(user_id, org_id, item, channel_id, #app_id)
    #    zoneid = 1
    #    coun =1
    #    ret, url_params,token = self._create_ysdk_order(ysdk.account_type,#app_id, app_key, open_id, open_key, pf, pf_key, zoneid, item, coun)
    #    if not ret:
    #        raise YsdkError.CREATE_ORDER_FAILED(user_id=user_id, item_id=org_id#, order_id=charge_log.cporderid,code=1)
    #    charge_log.taken_id = token
    #    charge_log.save()
#
    #    return {'url_params':url_params}


    @trace_service
    def create_charge_order_pay_m(self, user_id,channel_id, item_id):

        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        if item_id not in settings.YSDK.ysdk_items:
            raise YsdkError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        item = self._get_purchase_item(user_id, item_id)

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        charge_status = ChargeStatus()
        if not charge_status.can_charge(user_id, profile.vip_title, item_id):
            raise YsdkError.ITEM_HAS_CHARGED(user_id=user_id, item_id=item_id)

        try:
            ysdk = ysdk_models.Ysdk.get_ysdk_by_user_id(user_id=user_id)
        except YsdkError.USER_ID_NOT_EXIST:
            raise YsdkError.USER_ID_NOT_EXIST(user_id=user_id)
        app_id = settings.YSDK.qq_app_id
        if ysdk.account_type == '2':
            app_id = settings.YSDK.wx_app_id
        charge_log ,order_id= self._create_cp_order(user_id, org_id, item, channel_id, app_id)
        charge_log.save()
        return {'price': item.price,'transid':order_id}

    @trace_service
    def process_charge_order_pay_m(self, user_id, open_id, open_key, pf, pfkey, item_id,pay_token,transid):
        try:
            ysdk = ysdk_models.Ysdk.get_ysdk_by_user_id(user_id=user_id)
        except YsdkError.USER_ID_NOT_EXIST:
            raise YsdkError.USER_ID_NOT_EXIST(user_id=user_id)

        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        if item_id not in settings.YSDK.ysdk_items:
            raise YsdkError.ITEM_NOT_EXIST(user_id=user_id, item_id=item_id)
        item = self._get_purchase_item(user_id, item_id)
        ts = int(time.time())
        zoneid=1
        session_id = settings.YSDK.qq_session_id
        session_type = settings.YSDK.qq_session_type
        app_id = settings.YSDK.qq_app_id
        app_key = settings.YSDK.order_key
        if ysdk.account_type == '2':
            session_id = settings.YSDK.wx_session_id
            session_type = settings.YSDK.wx_session_type
            app_id = settings.YSDK.qq_app_id
            app_key = settings.YSDK.order_key
        cookies = dict(session_id=session_id, session_type=session_type, org_loc=settings.YSDK.org_loc)
        params = {
            'openid': str(open_id),
            'openkey': str(open_key),
            'appid': app_id,
            'billno': transid,
            'ts': str(ts),
            'pf': pf,
            'pfkey': pfkey,
            'zoneid': str(zoneid),
            'amt': str(item.price),
        }

        url_path = settings.YSDK.url_path
        sig = makesig.mksig(app_key, 'get', url_path, params)
        str_params = makesig.make_str_params(params)
        order_url = settings.YSDK.order_url
        order_url = '{0}?{1}&sig={2}'.format(order_url, str_params, sig)
        resp = requests.get(url=order_url, cookies=cookies)
        self.logger.debug('resp|%s', str(resp.content))
        if resp is None or resp.content is None or resp.content == '':
            raise YsdkError.NOT_SUFFICIENT_FUNDS(user_id=user_id)
        js = json.loads(resp.content.decode('string-escape').strip('"'))
        code = js['ret']
        if code != 0:
            raise YsdkError.NOT_SUFFICIENT_FUNDS(user_id=user_id)
        try:
            charge_log = ysdk_models.YsdkLog.get_ysdk_log_by_transid(transid)
            if charge_log.result == 1:
                self.logger.debug(
                    '[dianyou_charge] [orderid|%s] [amount|%s]  [other_id|%s] already exist',
                    transid, item.price, charge_log.id)
                raise YsdkError.ORDER_IS_USED(user_id=user_id,transid=transid)
        except Exception:
            raise YsdkError.ORDER_WROMG(user_id=user_id,transid=transid)

        if charge_log is None:
            self.logger.info("[orderid|%s]  is not exists in database", transid)
            raise YsdkError.NO_ORDER(user_id=user_id,transid=transid)

        item_id = int(charge_log.item_id)
        org_id = item_id
        if item_id in ITEMS.same_items:
            item_id = ITEMS.same_items[item_id].item_id
        user_id = int(charge_log.appuserid)
        item = self._get_purchase_item(user_id, item_id)
        store_service = StoreService(self.service_repositories, self.activity_repository)
        store_service.charge(user_id, org_id, 1, charge_log.channel_id, 'charge', transid,
                             revenue=int(item.price))

        charge_status = ChargeStatus()
        charge_status.charge(user_id, item_id)

        charge_log.money = item.price
        charge_log.result = 1
        charge_log.transtime = int(time.time())
        charge_log.transid = transid
        charge_log.save()
        try:
            player_charge = player_models.PlayerCharge.get_player_charge(user_id)
            money = player_charge.charge_money
            player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            player_charge.charge_money = money + item.price
            player_charge.save()
        except PlayerError.PLAYER_NOT_EXISTS:
            new_player_charge = player_models.PlayerCharge()
            new_player_charge.user_id = user_id
            new_player_charge.charge_times = time.strftime("%Y%m%d", time.localtime(time.time()))
            new_player_charge.charge_money = item.price
            new_player_charge.save()
        return {'result_code': 0}