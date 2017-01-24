__all__ = ['HuaweiBackend']
from go.containers.containers import Hash, Set

import ujson
import requests
import time
import traceback
import go.logging
from go.error import Error, Warning
from go.containers import redis
from card.core.conf import settings
from card.core.enum import Platform
from card.core.error.lobby import HuaweiError,HolyTreeError
import base64
from card.lobby.aop.logging import trace_service
from card.lobby.apps.holytree.backends import BaseBackend
from card.lobby.apps.holytree import models as holytree_models
from card.lobby.apps.player import models as player_models
from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.huawei.models import Huawei

@go.logging.class_wrapper
class HuaweiBackend(BaseBackend):

    def _login(self, access_token):

        '''
        result = json.loads(resp.content.decode('string-escape').strip('"'))

        recode = result["ResultCode"]
        recontent = result['Content']
        resign = result['Sign']
        sign = hashlib.md5(app_id + str(recode) + urllib.unquote(recontent) + secret_key).hexdigest()
        if recode != 1 or resign != sign or recontent is None or recontent == "":
            raise YuyangError.AUTH_FAILED(token=sessionid, code=recode)
            return

        content = urllib.unquote(recontent)
        content = base64.b64decode(content)
        content = ujson.loads(content)
        '''
        access_token = base64.b64decode(access_token)
        request_body={
        'nsp_svc':'OpenUP.User.getInfo',
        'nsp_ts' : time.time(),
        'access_token': access_token,
        }
        login_url = settings.HUAWEI.login_url
        resp = requests.post(login_url, data=request_body)
        if resp is None or resp == "" or resp.content is None or resp.content == "":
            return

        result = ujson.loads(resp.content.strip('"'))
        huawei_user_id = result['userID']
        self.logger.debug("[uid|%s]", huawei_user_id)
        return huawei_user_id

    @trace_service
    def authenticate(self, access_token,user_type,device_name, device_id, device_model,os_version, os_platform, app_version, channel, vender, login_ip, package_type,service_repositories, activity_repository, counter_repository, need_creation, **_):
        if user_type != 'huawei':
            raise TypeError("channel wrong")
        incompatible_versions = settings.HOLYTREE.incompatible_versions
        if (package_type in incompatible_versions and
            app_version in incompatible_versions[package_type]):
            raise HolyTreeError.incompatible_version()
        super(HuaweiBackend, self).authenticate(package_type, device_id, app_version)
        auth_resp = self._login(access_token)
        if auth_resp is None:
            return
        uid = int(auth_resp)
        assert uid is not None

        try:
            huawei = Huawei.get_huawei_by_uid(uid=uid)
            user_id = huawei.user_id
        except HuaweiError.UID_NOT_EXIST:
            self.logger.debug('[uid|%s] [device_id|%s] '
                '[app_version|%s] [device_name|%s] first login, now create',
                uid, device_id, app_version, device_name)
            nick_name = device_name
            user_id = self.create_new_player(uid, device_id, nick_name, app_version,
                          channel, vender, login_ip, package_type, os_version, os_platform,
                          service_repositories, activity_repository)
        except Exception as ex:
            self.logger.error(ex.message)
            traceback.print_exc()
            raise

        try:
            player_service = PlayerService(service_repositories, activity_repository)
            player_service.login(user_id)
            player = player_models.SessionPlayer(user_id)
        except Error as e:
            self.logger.error(e.message)
            raise
        except Warning as e:
            self.logger.warn(e.message)
            raise

        self.logger.debug('huawei [user_id|%s] [device_id|%s] [login_ip|%s]'
                '[uid|%s] [app_version|%s] [device_name|%s] authenticate successed',
                 user_id, device_id, login_ip, uid, app_version, device_name)
        #self._reset_fetch_time(user_id, service_repositories, activity_repository)

        return player

    def create_new_player(self, uid, device_id, nick_name, app_version,
                          channel, vender, login_ip, package_type, os_version, os_platform,
                          service_repositories, activity_repository):
        self._device_account_count(package_type,device_id)
        holytree_models.CreatePolicy.create_account(str(uid))
        try:
            player = super(HuaweiBackend, self).create_new_player(
                        device_id, nick_name, Platform.HUAWEI, channel, vender,
                        app_version, os_version, os_platform, login_ip, package_type,
                        service_repositories, activity_repository)

            ly = Huawei()
            ly.player = player
            ly.uid = int(uid)
            ly.save()
        except Exception:
            holytree_models.CreatePolicy.delete_account(int(uid))
            raise

        return player.user_id

    def _device_account_count(self, package_type, device_id):
        cfg = settings.HOLYTREE.create_device_limition.device_count
        re = redis.Redis(**settings.PERSIST_REDIS)
        key = cfg.create_device_key
        create_hash = Hash(key, re)
        value = create_hash.hget(device_id)
        return int(value) if value is not None else 0

    def _create_device_count_limitation(self, package_type, device_id):
        cfg = settings.HOLYTREE.create_device_limition.device_count
        if not cfg.active:
            return
        create_count = self._device_account_count(package_type, device_id)
        if create_count >= cfg.device_create_count:
            raise HolyTreeError.DEVICE_CREATE_TOO_MUCH(device_id=device_id)