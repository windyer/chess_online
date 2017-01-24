import hashlib
import ujson
import time
import traceback
import base64
import urllib
from Crypto.Cipher import AES

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.conf import settings

import go.logging
from go.containers.containers import Hash
from go.containers import redis

from card.core.error.lobby import HolyTreeError
from card.core.enum import Platform

from card.api.task.timeline_service import TimelineService as MailService
from card.lobby.service.view_service import ViewService
from card.lobby.aop.logging import trace_service
import card.lobby.apps.holytree.models as holytree_models

from card.lobby.apps.player import models as player_models
from card.lobby.apps.player.service import PlayerService
from card.core.util.timestamp import get_timestamp_for_now
from card.lobby.extensions.logging import mongo_logger
from random import sample


@go.logging.class_wrapper
class HolyTreeService(ViewService):
    def __init__(self, service_repositories, activity_repository, counter_repository):
        super(HolyTreeService, self).__init__(service_repositories, activity_repository)
        self.counter_repository = counter_repository

    def _send_reset_password_email(self, user_mail, token):
        subject = settings.HOLYTREE.reset_password.subject
        url = settings.HOLYTREE.reset_password.url_prefix.format(token)
        context = settings.HOLYTREE.reset_password.context.format(url)
        mail_service = MailService()
        mail_service.send_mail(subject, context, user_mail)
    def _send_check_email(self, user_mail, token,type):
        subject = settings.HOLYTREE.check_email.subject
        data = '{"user_mail":"%s","token":"%s","type":"%s"}' % (user_mail,token,type)
        parameter = base64.b64encode(data)
        url = settings.HOLYTREE.check_email.url_prefix.format(parameter)
        context = settings.HOLYTREE.check_email.context.format(url)
        mail_service = MailService()
        mail_service.send_mail(subject, context, user_mail)
    def check_token(self,user_email):
        token = settings.HOLYTREE.check_email.token_key_prefix.format(user_email, time.time())
        token = token.strip()
        encoded_token = hashlib.md5(token).hexdigest().upper()
        re = redis.Redis(**settings.PERSIST_REDIS)
        session_info = {}
        session_info["user_name"] = user_email
        re.setex(encoded_token, ujson.dumps(session_info), settings.HOLYTREE.check_email.token_expire_time)
        return encoded_token
    def send_email(self,user_id,user_email,password,type):
        #user=self.check_token(user_email)
        token = settings.HOLYTREE.check_email.token_key_prefix.format(user_email, time.time())
        token = token.strip()
        encoded_token = hashlib.md5(token).hexdigest().upper()
        re = redis.Redis(**settings.PERSIST_REDIS)
        session_info = {}
        session_info["user_name"] = user_email
        session_info["user_id"] = user_id
        session_info["password"] =password
        session_info["type"] =type
        session_info["temp"] = 0
        re.setex(encoded_token, ujson.dumps(session_info), settings.HOLYTREE.check_email.token_expire_time)
        self._send_check_email(user_email,encoded_token,type)
    def _decode_password(self, user_name, app_version, password):
        if app_version in settings.HOLYTREE.aes_keys:
            key = settings.HOLYTREE.aes_keys[app_version]
        else:
            key = settings.HOLYTREE.aes_keys["default"]

        try:
            cipher = AES.new(key, AES.MODE_ECB)
            decoderd_password = urllib.unquote(password)
            decoderd_password = cipher.decrypt(base64.b64decode(decoderd_password)).strip()
        except Exception as ex:
            self.logger.error(ex.message)
            traceback.print_exc()
            raise HolyTreeError.INVALID_PASSWORD(user_name=user_name, password=password)

        return decoderd_password

    @trace_service
    def change_password(self, user_id, password, new_password):
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        app_version = player_extra.app_version
        holytree = holytree_models.HolyTree.get_holytree_by_user_id(user_id=user_id)
        assert holytree is not None

        password = self._decode_password(holytree.user_name, app_version, password)
        new_password = self._decode_password(holytree.user_name, app_version, new_password)
        encodered_pwd = hashlib.md5(password).hexdigest()

        if encodered_pwd != holytree.password:
            raise HolyTreeError.AUTH_FAILED(user_name=holytree.user_name, password=encodered_pwd)

        new_pwd = hashlib.md5(new_password).hexdigest()
        holytree_models.HolyTree.update_password(user_id, new_pwd)

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        player_service.delete_session(user_id)

    @trace_service
    def reset_password(self, origin_token, new_password):
        token = origin_token.upper()
        re = redis.Redis(**settings.PERSIST_REDIS)
        if not re.exists(token):
            raise HolyTreeError.INVALID_TOKEN(token=origin_token)

        data = re.get(token)
        re.delete(token)
        data = ujson.loads(data)
        user_id = data["user_id"]
        user_name = data["user_name"]
        holytree = holytree_models.HolyTree.get_holytree_by_user_name(user_name=user_name)
        if holytree is None or holytree.user_id != user_id:
            raise HolyTreeError.INVALID_TOKEN(token=origin_token)

        new_pwd = hashlib.md5(new_password).hexdigest()
        holytree_models.HolyTree.update_password(holytree.user_id, new_pwd)

    @trace_service
    def forget_password(self, user_name):
        user_name = user_name.strip()
        user_name = user_name.lower()
        holytree = holytree_models.HolyTree.get_holytree_by_user_name(user_name=user_name)
        if holytree is None:
            raise HolyTreeError.USER_NAME_NOT_EXIST(user_name=user_name)

        re = redis.Redis(**settings.PERSIST_REDIS)
        forget_hash = Hash(settings.HOLYTREE.reset_password.last_forget_password_key)
        last_forget_time = forget_hash.hget(holytree.user_id)
        last_forget_time = int(last_forget_time) if last_forget_time else 0
        if int(time.time()) - last_forget_time < settings.HOLYTREE.reset_password.forget_password_interval:
            raise HolyTreeError.FORGET_PASSWORD_FREQUENTLY(user_name=user_name)

        forget_hash.hset(holytree.user_id, int(time.time()))
        token = settings.HOLYTREE.reset_password.token_key_prefix.format(user_name, time.time())
        token = token.strip()
        encoded_token = hashlib.md5(token).hexdigest().upper()

        session_info = {}
        session_info["user_id"] = holytree.user_id
        session_info["user_name"] = user_name
        re.setex(encoded_token, ujson.dumps(session_info), settings.HOLYTREE.reset_password.token_expire_time)
        self._send_reset_password_email(user_name, encoded_token)

    def check_email(self,token):
        re = redis.Redis(**settings.PERSIST_REDIS)
        if not re.exists(token):
            return 0
        data = re.get(token)
        data = ujson.loads(data)
        if data['temp'] == 0:
            self.bind_account(data['user_id'],data['user_name'],data['password'])
            data['temp'] = 1
            re.setex(token, ujson.dumps(data), settings.HOLYTREE.check_email.token_expire_time)
            return 1
        else :
            return 0


    def bind_account(self, user_id, user_name, password):
        user_name = user_name.strip()
        user_name = user_name.lower()
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        app_version = player_extra.app_version
        password = self._decode_password(user_name, app_version, password)

        try:
            guest = holytree_models.Guest.get_guest_by_user_id(user_id=user_id)
        except HolyTreeError.USER_ID_NOT_EXIST:
            raise HolyTreeError.USER_ALREADY_BIND(user_id=user_id)

        try:
            holytree = holytree_models.HolyTree.get_holytree_by_user_name(user_name=user_name)
        except HolyTreeError.USER_NAME_NOT_EXIST:
            holytree = holytree_models.HolyTree()
            holytree.player = player_models.Player.objects.get(pk=user_id)
            holytree.user_name = user_name
            holytree.password = hashlib.md5(password).hexdigest()
            try:
                holytree.save()
            except Exception as ex:
                print ex
                return
            player_extra = player_models.PlayerExtra.get_player_extra(user_id)
            assert player_extra is not None
            player_extra.player_type = Platform.HOLYTREE
            player_models.PlayerExtra.update_player_extra(player_extra)
        else:
            raise HolyTreeError.USER_NAME_ALREADY_EXIST(user_name=user_name)

        holytree_models.Guest.delete_guest(guest)
        for counter in self.counter_repository.counters:
            counter.incr(holytree.player.user_id, **{'bind_account':1})
        

@receiver(user_logged_in, sender=player_models.SessionPlayer)
def login_log(sender, user, request, **kwargs):
    device_id = request.POST.get('device_id', None)
    device_name = request.POST.get('device_name', None)
    app_version = request.POST.get('app_version', None)
    os_version = request.POST.get('os_version', None)
    package_type = request.POST.get('package_type', None)
    login_ip = request.META.get('REMOTE_ADDR', None)
    vender = request.POST.get('vender', None)
    networking = request.POST.get('networking', None)
    resolution = request.POST.get('resolution', None)
    imei_number = request.POST.get('imei_number', None)
    channel = request.POST.get('channel', None)

    player_service = PlayerService(request.service_repositories, 
                                request.activity_repository)
    version_updated = player_service.update_last_login(
        user.id, device_id, app_version, login_ip, package_type,
        vender, networking, resolution, imei_number, os_version,
        request.session, channel
    )

    player = player_models.Player.get_player(user.id)
    mongo_logger.player_login(
        user_id=user.id,
        nick_name=request.POST.get('nick_name', device_name),
        currency=player.currency,
        device_id=device_id,
        device_name=device_name,
        device_model=request.POST.get('device_model', None),
        app_version=app_version,
        version_updated=version_updated,
        login_ip=login_ip,
        os_version=os_version,
        channel=request.POST.get('channel', None),
        vender=vender,
        timestamp=get_timestamp_for_now(unit='ms')
    )
