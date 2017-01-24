__all__ = ['ChubaoBackend']

import hmac
import hashlib
import ujson
import requests

import traceback

import go.logging
from go.error import Error, Warning

from card.core.conf import settings
from card.core.enum import Platform
from card.core.error.lobby import ChubaoError,HolyTreeError

from card.lobby.aop.logging import trace_service
from card.lobby.apps.holytree.backends import BaseBackend
from card.lobby.apps.holytree import models as holytree_models
from card.lobby.apps.player import models as player_models
from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.chubao.models import Chubao


@go.logging.class_wrapper
class ChubaoBackend(BaseBackend):

    def _login(self, sessionid):
        '''
        result = json.loads(resp.content.decode('string-escape').strip('"'))

        recode = result["ResultCode"]
        recontent = result['Content']
        resign = result['Sign']
        sign = hashlib.md5(app_id + str(recode) + urllib.unquote(recontent) + secret_key).hexdigest()
        if recode != 1 or resign != sign or recontent is None or recontent == "":
            raise ChubaoError.AUTH_FAILED(token=sessionid, code=recode)
            return

        content = urllib.unquote(recontent)
        content = base64.b64decode(content)
        content = ujson.loads(content)
        '''
        chubao_user_id = sessionid
        self.logger.debug("[sessionid|%s] [uid|%s]", sessionid, chubao_user_id)
        return chubao_user_id

    @trace_service
    def authenticate(self, user_name, sessionId, device_name, device_id, device_model,os_version, os_platform, app_version, channel, vender, login_ip, package_type,service_repositories, activity_repository, counter_repository, need_creation, **_):
        self.logger.debug("[session|%s]", sessionId)
        if channel != settings.CHUBAO.channel:
            raise TypeError("channel wrong")
        incompatible_versions = settings.HOLYTREE.incompatible_versions
        if (package_type in incompatible_versions and
            app_version in incompatible_versions[package_type]):
            raise HolyTreeError.incompatible_version()

        super(ChubaoBackend, self).authenticate(package_type, device_id, app_version)

        auth_resp = None

        auth_resp = self._login(sessionId)
        if auth_resp is None:
            return
        uid = int(auth_resp)
        assert uid is not None

        try:
            chubao = Chubao.get_chubao_by_uid(uid=uid)
            user_id = chubao.user_id
        except ChubaoError.UID_NOT_EXIST:
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

        self.logger.debug('chubao [user_id|%s] [device_id|%s] [login_ip|%s]'
                '[uid|%s] [app_version|%s] [device_name|%s] authenticate successed',
                 user_id, device_id, login_ip, uid, app_version, device_name)
        #self._reset_fetch_time(user_id, service_repositories, activity_repository)

        return player

    def create_new_player(self, uid, device_id, nick_name, app_version,
                          channel, vender, login_ip, package_type, os_version, os_platform,
                          service_repositories, activity_repository):
        holytree_models.CreatePolicy.create_account("chubao" + str(uid))
        try:
            player = super(ChubaoBackend, self).create_new_player(
                        device_id, nick_name, Platform.BAIDU, channel, vender,
                        app_version, os_version, os_platform, login_ip, package_type,
                        service_repositories, activity_repository)

            ly = Chubao()
            ly.player = player
            ly.uid = str(uid)
            ly.save()
        except Exception:
            holytree_models.CreatePolicy.delete_account("chubao" + str(uid))
            raise

        return player.user_id
