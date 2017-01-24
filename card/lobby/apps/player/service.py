# coding=utf-8

import time
import collections
import datetime
import uuid
import hashlib
import base64
import traceback
import urllib
import ujson
from Crypto.Cipher import AES
from datetime import timedelta

from django.utils import timezone
from django.conf import settings

from go.containers import redis
from go.containers.containers import Hash
from go.util import DotDict
import go.logging
from card.lobby.settings import activity

from card.core.charge import ITEMS
from card.core.statistics.models import StatisticItem, MonthStatisticItem, DailyStatisticItem
from card.core.property.three import Property
from card.core.enum import IdentifyType

from card.api.task.timeline_service import TimelineService as MailService

from card.lobby.service.view_service import ViewService
from card.lobby.aop import args_limit
from card.lobby.aop.logging import trace_service
from card.lobby.extensions.logging import mongo_logger
from card.core.util.timestamp import get_timestamp_for_now

import card.lobby.apps.player.models as player_models
from card.lobby.apps.activity.base import ActivityHandler
from card.lobby.apps.player.redis import PlayerAlbum
from card.core.error.lobby import PlayerError
from card.lobby.apps.player.player_event import PlayerEvent
import card.lobby.apps.holytree.models as holytree_models
import ac_dict
import re
from card.core.util.sensitive_filter import numeric_filter,symbol2num,del_special,trans,del_special_special
from card.lobby.apps.player.models import Player
current_timezone = timezone.get_current_timezone()

class SensitiveFilter(object):
    _instance = None

    def __init__(self):
        self._ac_dict = ac_dict.AC_Dict(settings.SENSITIVE_WORDS_FILE)

    @staticmethod
    def filter(words):
        if SensitiveFilter._instance is None:
            SensitiveFilter._instance = SensitiveFilter()
        if words is None or words == '':
            return words
        text = words.encode('utf-8')
        #return numeric_filter(text)
        #words = SensitiveFilter._ac_dict.filter(words.encode("utf-8")).decode('utf-8')
        #acdict = ac_dict.AC_Dict(settings.SENSITIVE_WORDS_FILE)
        text = symbol2num(text)
        del_text = del_special(text)
        cn2dig = trans(del_text)
        filtered_text = SensitiveFilter._instance._ac_dict.filter(cn2dig)
        filtered_text = numeric_filter(filtered_text)
        if cn2dig == filtered_text:
            del_text = del_special_special(text)
            cn2dig = trans(del_text)
            filtered_text = SensitiveFilter._instance._ac_dict.filter(cn2dig)
            filtered_text = numeric_filter(filtered_text)
            if filtered_text == cn2dig:
                filtered_text = text
        return filtered_text

@go.logging.class_wrapper
class PlayerService(ViewService):

    def _is_robot(self, user_id):
        profile = self.get_profile(user_id)
        return profile.is_robot

    def get_charge_moneys(self, user_id, last_days):
        assert last_days >= 0

        charge_moneys = []
        today = datetime.date.today()
        day = 0
        while day <= last_days:
            statistics = DailyStatisticItem(today - timedelta(days=day))
            statistics.set_id(user_id)
            stat = collections.defaultdict(int, statistics.counters_value)
            charge_moneys.append(stat['charge_money'])
            day += 1

        return charge_moneys

    def _send_reset_password_email(self, user_mail, token):
        subject = settings.PLAYER.reset_password.subject
        url = settings.PLAYER.reset_password.url_prefix.format(token)
        context = settings.PLAYER.reset_password.context.format(url)
        mail_service = MailService()
        mail_service.send_mail(subject, context, user_mail)

    def _give_monthly_charge(self, user_id, player_extra, first_login_this_month):
        charge_item_id = Property.MONTHLY_FIFTEEN_RMB_COINS.item_id
        if first_login_this_month:
            from card.lobby.apps.store.service import StoreService
            store_service = StoreService(self.service_repositories, self.activity_repository)
            store_service.charge(user_id, charge_item_id, 1, player_extra.channel, 'monthly_payment')
        else:
            item = ITEMS.monthly_coins[Property.MONTHLY_FIFTEEN_RMB_COINS]
            self.increment_currency(user_id, item.coin, "monthly_payment")
            player_event = PlayerEvent(self.service_repositories, self.activity_repository)
            player_event.send_monthly_payment_event(user_id, charge_item_id)

    def delete_session(self, user_id):
        re = redis.Redis(**settings.CACHE_REDIS)
        user_session_key = settings.SESSION_MAPPING_KEY.format(user_id=user_id)
        session_id = re.get(user_session_key)
        session_key = settings.SESSION_REDIS_PREFIX + ':' + str(session_id)

        if re.exists(session_key):
            re.delete(session_key)
        if re.exists(user_session_key):
            re.delete(user_session_key)

    def _nick_name_check(self, user_id, new_nick_name):
        if len(new_nick_name) <= 0:
            raise PlayerError.INVALID_NICK_NAME(user_id=user_id, nick_name=new_nick_name)

        if new_nick_name in settings.PLAYER.exclude_nick_names:
            return

        re = redis.Redis(**settings.PERSIST_REDIS)
        nick_name_hash = Hash(settings.PLAYER.nick_name_hash_key, re)

        nick_name_count = nick_name_hash.hget(new_nick_name)
        nick_name_count = int(nick_name_count) if nick_name_count is not None else 0
        if nick_name_count > 0:
            raise PlayerError.NICK_NAME_USED_ALREADY(user_id=user_id, nick_name=new_nick_name)

        real_count = nick_name_hash.hincrby(new_nick_name)
        if real_count > 1:
            raise PlayerError.NICK_NAME_USED_ALREADY(user_id=user_id, nick_name=new_nick_name)

    def _rollback_nick_name(self, new_nick_name):
        if new_nick_name in settings.PLAYER.exclude_nick_names:
            return

        re = redis.Redis(**settings.PERSIST_REDIS)
        nick_name_hash = Hash(settings.PLAYER.nick_name_hash_key, re)
        nick_name_hash.hdel(new_nick_name)

    def _del_older_nick_name(self, nick_name):
        re = redis.Redis(**settings.PERSIST_REDIS)
        nick_name_hash = Hash(settings.PLAYER.nick_name_hash_key, re)
        nick_name_hash.hdel(nick_name)

    def deactive_account(self, user_id, reason):
        self.update_profile(user_id, is_active=False)
        self.logger.info("[auto deactive] [user|%d] for max logon device count", user_id)
        self.delete_session(user_id)

        log = player_models.AutoDeactiveLog()
        log.user_id = user_id
        log.reason = reason
        log.save()

    def has_charged_coin(self, user_id):
        re = redis.Redis(**settings.PERSIST_REDIS)
        key = settings.ACTIVITY.charge_player_key.format(user_id)
        charge_status_hash = Hash(key, re)
        json_value = charge_status_hash.hget(user_id)
        charge_status = None
        if json_value is not None:
            charge_status = collections.defaultdict(int, ujson.loads(json_value))
        else:
            charge_status = collections.defaultdict(int) 

        return charge_status["coins"] > 0

    def get_property_items(self, user_id):
        assert user_id is not None
        property_service = self.service_repositories.db.property_service
        resp = property_service.get_items(user_id)
        items = [{'item_id': item.item_id, 'count': item.count}
                 for item in resp.items]

        return items

    def get_albums(self, user_id, myself):
        rplayer_album = PlayerAlbum.objects.get_by_id(user_id)
        if rplayer_album is None:
            return []

        albums = rplayer_album.albums
        if myself:
            pending = rplayer_album.pending
            for image_id in pending.keys():
                pending[image_id] = '0'
            albums.update(pending)

        resp = []
        for image_id, image_url in albums.iteritems():
            resp.append({'image_id': image_id, 'image_url': image_url})
        return resp

    def update_album(self, user_id, image_id, image_url):
        rplayer_album = PlayerAlbum.objects.get_by_id(user_id)
        if rplayer_album is None:
            rplayer_album = PlayerAlbum()
            rplayer_album.set_id(user_id)
        rplayer_album.pending[image_id] = image_url
        rplayer_album.save()

    def update_audited_album(self, user_id, image_id, counter_repository,
                             image_url=None):
        rplayer_album = None
        if image_url is None:
            rplayer_album = PlayerAlbum.objects.get_by_id(user_id)
            image_url = rplayer_album.pending.pop(image_id, '')
        if image_id == 0:
            self.update_profile(user_id, avatar_url=image_url)
        else:
            rplayer_album.albums[image_id] = image_url
        if rplayer_album != None:
            rplayer_album.save()

        if not image_url.startswith("http://") and not image_url.startswith("https://"):
            return
        for counter in counter_repository.counters:
            counter.incr(user_id, **{'update_avatar_time':1})

    def delete_album(self, user_id, image_id):
        rplayer_album = PlayerAlbum.objects.get_by_id(user_id)
        if rplayer_album is None:
            return

        if image_id in rplayer_album.pending:
            rplayer_album.pending.pop(image_id)
        else:
            assert image_id in rplayer_album.albums
            rplayer_album.albums.pop(image_id)

        rplayer_album.save()

    def update_avatar(self, user_id, image_id):
        rplayer_album = PlayerAlbum.objects.get_by_id(user_id)
        if rplayer_album is None:
            raise PlayerError.PLAYER_ALBUM_EMPTY(user_id=user_id)
        albums = rplayer_album.albums
        if image_id not in albums:
            raise PlayerError.IMAGE_ID_NOT_EXISTS(user_id=user_id, image_id=image_id)

        user_profile = self.get_profile(user_id)
        image_url = albums[image_id]
        self.update_profile(user_id, avatar_url=image_url)

        albums[image_id] = user_profile.avatar_url
        rplayer_album.save()

        self.logger.info('avatar_url_trace [user|%d] modify '
                        '[avatar_url|%s] to [avatar_url|%s]', 
                        user_id, user_profile.avatar_url, image_url)

    def is_avatar_audit_pending(self, user_id):
        rplayer_album = PlayerAlbum.objects.get_by_id(user_id)
        return rplayer_album and 0 in rplayer_album.pending

    def get_month_statistic(self, user_id):
        statistics = MonthStatisticItem()
        statistics.set_id(user_id)
        return statistics.counters_value

    def update_identify_time(self, user_id, identify_type):
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)

        has_identified_today = player_extra.has_identified_today
        if player_extra.app_version >= "1.0.0":
            player_extra.last_identify_time = timezone.now()
            player_models.PlayerExtra.update_player_extra(player_extra)

        award_currency = 0
        if not has_identified_today and identify_type == IdentifyType.IDIOM:
            award_currency = settings.PLAYER.idiom_identify_award
            self.increment_currency(user_id, award_currency, 'idiom_identify_award')
        return award_currency

    def update_last_login(self, user_id, device_id, app_version, login_ip, package_type,
                        vender, networking, resolution, imei_number, os_version, session, channel):
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)

        if settings.PLAYER.identify:
            if player_extra.has_identified_today:
                session["is_identified"] = True
            else:
                session["is_identified"] = False
        else:
            session["is_identified"] = True

        if app_version > "9.5.0":
            session["identify_type"] = IdentifyType.IDIOM
        else:
            session["identify_type"] = IdentifyType.NUMBER

        first_login_today = False
        first_login_this_month = False
        if not player_extra.has_logined_today:
            first_login_today = True
            if not player_extra.has_logined_this_month:
                first_login_this_month = True
            if player_extra.last_login_time is None:
                player_extra.continuous_login_days = 1
            else:
                last_login = player_extra.last_login_time.astimezone(current_timezone)
                yesterday = timezone.datetime.now() - timezone.timedelta(days=1)
                if (last_login.year == yesterday.year
                      and last_login.month == yesterday.month
                      and last_login.day == yesterday.day):
                    player_extra.continuous_login_days += 1
                else:
                    player_extra.continuous_login_days = 1

        version_updated = False
        if not self._is_robot(user_id):
            player_extra.login_ip = login_ip
            if player_extra.app_version and app_version:
                version_updated = self.is_app_version_updated(
                    player_extra.app_version, app_version
                )

        if player_extra.app_version != app_version:
            try:
                player_service = self.service_repositories.db.player_service
                player_service.update_app_version(user_id=user_id, app_version=app_version)
            except Exception as ex:
                print ex
                pass
        if player_extra.channel != channel:
            try:
                player_service = self.service_repositories.db.player_service
                player_service.update_channel(user_id=user_id, channel=channel)
            except Exception as ex:
                print ex
                pass

        player_extra.app_version = app_version
        player_extra.package_type = package_type
        player_extra.login_device_id = device_id
        player_extra.last_login_time = timezone.now()
        player_extra.token = hashlib.md5(str(time.time())).hexdigest()
        player_extra.vender = vender
        player_extra.os_version = os_version
        player_extra.networking = networking
        player_extra.resolution = resolution
        player_extra.imei_number = imei_number
        player_extra.channel = channel
        if first_login_today and player_extra.is_monthly_player:
            self._give_monthly_charge(user_id, player_extra, first_login_this_month)
        elif not player_extra.is_monthly_player:
            player_extra.monthly_payment = False;

        player_models.PlayerExtra.update_player_extra(player_extra)
        ActivityHandler.process_logon(user_id=user_id, 
                            service_repositories=self.service_repositories, 
                            activity_repository=self.activity_repository, 
                            context=DotDict({'device_id':device_id,
                                            'first_login_today':first_login_today}))

        self.logger.info('[user|%d] [func|update_last_login] '
                         '[last_login|%s][continuous_login_days|%d]',
                         user_id, player_extra.last_login_time,
                         player_extra.continuous_login_days)
        return version_updated

    @trace_service
    @args_limit('nick_name', 'gender', 'signature', 'avatar_url', 'is_active', 'contact')
    def update_profile(self, user_id, **kwargs):
        user_profile = self.get_profile(user_id)
        if 'nick_name' in kwargs:
            new_nick_name = kwargs["nick_name"].strip()
            self._nick_name_check(user_id, new_nick_name)
            self.logger.info('nick_name_trace [user|%d] modify '
                            '[nick_name|%s] to [nick_name|%s]',
                            user_id, user_profile.nick_name, kwargs['nick_name'])

        try:
            player_service = self.service_repositories.db.player_service
            player_service.update_profile(user_id=user_id, **kwargs)
        except Exception:
            if 'nick_name' in kwargs:
                self._rollback_nick_name(new_nick_name)
            raise

        if 'nick_name' in kwargs:
            self._del_older_nick_name(user_profile.nick_name)

    def get_profile(self, user_id):
        player_service = self.service_repositories.db.player_service
        return player_service.get_profile(user_id)

    def get_profiles(self, *users_id):
        player_service = self.service_repositories.db.player_service
        user_profiles = player_service.get_profiles(*users_id)

        return user_profiles.profiles

    def login(self, user_id):
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        is_monthly_player = player_extra.is_monthly_player
        return self.service_repositories.db.player_service.login(user_id, is_monthly_player)

    @trace_service
    def increment_currency(self, user_id, delta, reason):
        assert delta > 0
        player_service = self.service_repositories.db.player_service
        transaction_id = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()

        self.trans_logger.info('[user|%d] pre [increment_currency|%d] [reason|%s] '
                    'with [transaction|%s]', user_id, delta, reason, transaction_id)
        response = player_service.increment_currency(user_id, transaction_id, delta)
        self.trans_logger.info('[user|%d] post [increment_currency|%d] [reason|%s] '
                    'with [transaction|%s]', user_id, delta, reason, transaction_id)

        extra = player_models.PlayerExtra.get_player_extra(user_id)
        mongo_logger.currency_issue(
            user_id=user_id, delta=delta, reason=reason, channel=extra.channel,
            timestamp=get_timestamp_for_now(unit='ms')
        )

        return response

    @trace_service
    def decrement_cat_food(self, user_id,cat_weight):
        assert cat_weight >= 0
        player_service = self.service_repositories.db.player_service
        response = player_service.decrement_cat_food(user_id,cat_weight)
        return response
        
    @trace_service
    def admin_increment_currency(self, user_id, delta, reason):
        assert delta > 0
        player_service = self.service_repositories.db.player_service
        transaction_id = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()

        self.trans_logger.info('[user|%d] pre [admin_increment_currency|%d] [reason|%s] '
                    'with [transaction|%s]', user_id, delta, reason, transaction_id)
        response = player_service.admin_increment_currency(user_id, transaction_id, delta)
        self.trans_logger.info('[user|%d] post [admin_increment_currency|%d] [reason|%s] '
                    'with [transaction|%s]', user_id, delta, reason, transaction_id)

        extra = player_models.PlayerExtra.get_player_extra(user_id)
        mongo_logger.currency_issue(
            user_id=user_id, delta=delta, reason=reason, channel=extra.channel,
            timestamp=get_timestamp_for_now(unit='ms')
        )

        return response

    @trace_service
    def decrement_currency(self, user_id, delta, reason):
        assert delta > 0
        player_service = self.service_repositories.db.player_service
        transaction_id = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()

        self.trans_logger.info('[user|%d] pre [decrement_currency|%d] [reason|%s] '
                    'with [transaction|%s]', user_id, delta, reason, transaction_id)
        response = player_service.decrement_currency(user_id, transaction_id, delta)
        self.trans_logger.info('[user|%d] post [decrement_currency|%d] [reason|%s] '
                    'with [transaction|%s]', user_id, delta, reason, transaction_id)

        extra = player_models.PlayerExtra.get_player_extra(user_id)
        mongo_logger.currency_withdrawal(
            user_id=user_id, delta=delta, reason=reason, channel=extra.channel,
            timestamp=get_timestamp_for_now(unit='ms')
        )

        return response

    @trace_service
    def deposit_currency(self, user_id, delta, auto_deposit):
        assert delta > 0
        if auto_deposit == True:
            commission = 0
        else:
            commission_ratio = settings.PLAYER.bank_commission
            commission = int(delta * commission_ratio)
            if commission > settings.PLAYER.max_bank_commission:
                commission = settings.PLAYER.max_bank_commission
        player_service = self.service_repositories.db.player_service
        transaction_id = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()

        self.trans_logger.info('[user|%d] pre [deposit_currency|%d] '
                    'with [transaction|%s]', user_id, delta, transaction_id)
        response = player_service.deposit_currency(user_id, transaction_id, delta, commission)
        self.trans_logger.info('[user|%d] post [deposit_currency|%d] '
                    'with [transaction|%s]', user_id, delta, transaction_id)

        return response

    @trace_service
    def withdraw_currency(self, user_id, delta, password):
        assert delta > 0
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        app_version = player_extra.app_version

        if app_version in settings.HOLYTREE.aes_keys:
            key = settings.HOLYTREE.aes_keys[app_version]
        else:
            key = settings.HOLYTREE.aes_keys["default"]

        try:
            cipher = AES.new(key, AES.MODE_ECB)
            password = urllib.unquote(password)
            password = cipher.decrypt(base64.b64decode(password)).strip()
        except Exception as ex:
            self.logger.error(ex.message)
            traceback.print_exc()
            raise PlayerError.INVALID_PASSWORD(user_id=user_id, password=password)

        encodered_pwd = hashlib.md5(password).hexdigest()
        if encodered_pwd != player_extra.bank_password:
            raise PlayerError.BANK_PASSWORD_AUTH_FAILED(user_id=user_id, password=encodered_pwd)

        player_service = self.service_repositories.db.player_service
        transaction_id = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()

        self.trans_logger.info('[user|%d] pre [withdraw_currency|%d] '
                    'with [transaction|%s]', user_id, delta, transaction_id)
        response = player_service.withdraw_currency(user_id, transaction_id, delta)
        self.trans_logger.info('[user|%d] post [withdraw_currency|%d] '
                    'with [transaction|%s]', user_id, delta, transaction_id)

        return response

    @trace_service
    def change_bank_password(self, user_id, password, new_password):
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        app_version = player_extra.app_version
        key = settings.HOLYTREE.aes_keys['default']
        if app_version in settings.HOLYTREE.aes_keys:
            key = settings.HOLYTREE.aes_keys[app_version]
        try:
            cipher = AES.new(key, AES.MODE_ECB)
            password = urllib.unquote(password)
            password = cipher.decrypt(base64.b64decode(password)).strip()
            new_password = urllib.unquote(new_password)
            new_password = cipher.decrypt(base64.b64decode(new_password)).strip()
        except Exception as ex:
            self.logger.error(ex.message)
            traceback.print_exc()
            raise PlayerError.INVALID_PASSWORD(user_id=user_id, password=password)

        encodered_pwd = hashlib.md5(password).hexdigest()
        if encodered_pwd != player_extra.bank_password:
            raise PlayerError.BANK_PASSWORD_AUTH_FAILED(user_id=user_id, password=encodered_pwd)

        new_pwd = hashlib.md5(new_password).hexdigest()
        player_extra.bank_password = new_pwd
        player_models.PlayerExtra.update_player_extra(player_extra)

    @trace_service
    def forget_bank_password(self, user_id):
        holytree = holytree_models.HolyTree.get_holytree_by_user_id(user_id=user_id)
        if holytree is None:
            raise HolyTreeError.USER_ID_NOT_EXIST(user_id=user_id)

        re = redis.Redis(**settings.PERSIST_REDIS)
        forget_hash = Hash(settings.PLAYER.reset_password.last_forget_password_key)
        last_forget_time = forget_hash.hget(user_id)
        last_forget_time = int(last_forget_time) if last_forget_time else 0
        if int(time.time()) - last_forget_time < settings.PLAYER.reset_password.forget_password_interval:
            raise PlayerError.FORGET_BANK_PASSWORD_FREQUENTLY(user_id=user_id)

        forget_hash.hset(user_id, int(time.time()))
        token = settings.PLAYER.reset_password.token_key_prefix.format(user_id, time.time())
        token = token.strip()
        encoded_token = hashlib.md5(token).hexdigest().upper()

        user_name = holytree.user_name
        user_name = user_name.strip()
        user_name = user_name.lower()

        session_info = {}
        session_info["user_id"] = user_id
        session_info["user_name"] = user_name
        re.setex(encoded_token, ujson.dumps(session_info), settings.PLAYER.reset_password.token_expire_time)
        self._send_reset_password_email(user_name, encoded_token)

    @trace_service
    def reset_bank_password(self, origin_token, new_password):
        token = origin_token.upper()
        re = redis.Redis(**settings.PERSIST_REDIS)
        if not re.exists(token):
            raise PlayerError.INVALID_TOKEN(token=origin_token) 

        data = re.get(token)
        re.delete(token)
        data = ujson.loads(data)
        user_id = data["user_id"]
        user_name = data["user_name"]
        holytree = holytree_models.HolyTree.get_holytree_by_user_name(user_name=user_name)
        if holytree is None or holytree.user_id != user_id:
            raise PlayerError.INVALID_TOKEN(token=origin_token)

        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        new_pwd = hashlib.md5(new_password).hexdigest()
        player_extra.bank_password = new_pwd
        player_models.PlayerExtra.update_player_extra(player_extra)

    @trace_service
    def get_bank_details(self, user_id):
        player_service = self.service_repositories.db.player_service
        return player_service.get_bank_details(user_id=user_id)

    @trace_service
    def draw_vip_bag_award(self, user_id, vip_title):
        profile = self.get_profile(user_id)
        if profile.vip_title < vip_title or vip_title <= 0:
            raise PlayerError.VIP_BAG_NOT_REACH_LIMIT(user_id=user_id, vip_title=vip_title)

        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        if player_extra.vip_award_steps:
            awarded_vip_titles = ujson.loads(player_extra.vip_award_steps)
        else:
            awarded_vip_titles = []

        if vip_title in awarded_vip_titles:
            raise PlayerError.VIP_BAG_HAS_AWARDED(user_id=user_id, vip_title=vip_title)

        award_items = settings.VIP.vip_bags[vip_title]
        player_service = PlayerService(self.service_repositories, self.activity_repository)
        for item in award_items:
            if item.count <= 0:
                continue
            if item.item_id == Property.COIN:
                player_service.increment_currency(user_id, item.count, reason)
            else:
                player_service.increment_item(user_id, item.item_id, item.count)

        awarded_vip_titles.append(vip_title)
        player_extra.vip_award_steps = ujson.dumps(awarded_vip_titles)
        player_models.PlayerExtra.update_player_extra(player_extra)


        resp = {}
        resp['vip_award_steps'] = awarded_vip_titles
        resp['bag_awards'] = award_items

        from card.lobby.apps.timeline.service import TimeLineService
        vip_name = settings.PLAYER.vip_titles[vip_title]
        message = settings.PLAYER.vip_bag_msg.format(vip_name)
        timeline_service = TimeLineService(self.service_repositories, self.activity_repository)
        timeline_service.send_personal_message(user_id, message)

        return resp

    def increment_item(self, user_id, item_id, count):
        transaction_id = hashlib.md5(uuid.uuid1().get_hex()).hexdigest()
        self.trans_logger.info(
            '[user|%d] pre [increment_item|%d] [count|%d] with [transaction|%s]',
            user_id, item_id, count, transaction_id)
        property_service = self.service_repositories.db.property_service
        response = property_service.increment_item(user_id, transaction_id, item_id, count)
        self.trans_logger.info(
            '[user|%d] post [increment_item|%d] [count|%d] with [transaction|%s]',
            user_id, item_id, count, transaction_id)

        return response

    def logout(self, user_id):
        return self.service_repositories.db.player_service.logout(user_id)

    def reset_gamed_time(self, user_id):
        return self.service_repositories.db.player_service.reset_gamed_time(user_id=user_id) 

    def report_player(self, user_id, target_user_id, reason, context):
        report_log = player_models.ReportLog()
        report_log.user_id = user_id
        report_log.target_user_id = target_user_id
        report_log.reason = reason
        report_log.context = context
        report_log.save()

    def is_app_version_updated(self, origin_version, login_version):
        origin_version = map(int, origin_version.split('.'))
        login_version = map(int, login_version.split('.'))

        return login_version > origin_version

    def get_highest_award(self):
        response = {}
        bulletin_service = self.service_repositories.chat.bulletin_service
        try:
            first_award = bulletin_service.get_first_award()
            if first_award.turner is not None:
                m = first_award.turner
                response['turner'] = {'user_id':m.user_id, 'nick_name':m.nick_name, 'currency':m.currency}
            if first_award.three is not None:
                m = first_award.three
                response['three'] = {'user_id':m.user_id, 'nick_name':m.nick_name, 'currency':m.currency}
            if first_award.fruit is not None:
                m = first_award.fruit
                response['fruit'] = {'user_id':m.user_id, 'nick_name':m.nick_name, 'currency':m.currency}
        except Exception as ex:
            pass
        return response

    def get_bull_download_count(self):
        re = redis.Redis(**settings.PERSIST_REDIS)
        result = re.get(settings.BULL_URL.download_count_key)
        if result is None:
            result = 0
        result = int(int(result) * settings.BULL_URL.download_count_pro)
        return result

    def get_game_min_cash(self):
        return settings.GAME.game_min_cash

    def get_date_gift(self):
        if time.strftime("%Y%m%d", time.localtime(time.time())) <= activity.ACTIVITY['double_seventh']['end_time'] and time.strftime("%Y%m%d", time.localtime(time.time())) >= activity.ACTIVITY['double_seventh']['start_time']:
            re = redis.Redis(**settings.PERSIST_REDIS)
            male = re.zrange('activity_male', -1, -1)
            female = re.zrange('activity_female', -1, -1)
            male_name=''
            male_id=''
            female_name=''
            female_id=''
            if len(male):
                male_id = male[0]
                male = Player.get_player(male[0])
                male_name = male.nick_name

            if len(female):
                female_id = female[0]
                female = Player.get_player(female[0])
                female_name = female.nick_name
            first_person = {"male_id":male_id,"male_name":male_name,"female_id":female_id,"female_name":female_name}
        else:
            first_person={}
        return first_person

    @trace_service
    def luck_bag(self, user_id, click_time):
        player_service = self.service_repositories.db.player_service
        response = player_service.luck_bag(user_id, click_time)
        self.trans_logger.info('[user|%d] post [click_time|%s] ', user_id, click_time)
        #mongo_logger.currency_issue(
            #user_id=user_id, delta=delta, reason=reason, channel=extra.channel,
            #timestamp=get_timestamp_for_now(unit='ms')
        #)
        return response

