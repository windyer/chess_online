__all__ = ['CoolpadBackend']
import ujson
import requests
from go.containers import redis
import traceback
import go.logging
from go.error import Error, Warning

from card.core.conf import settings
from card.core.enum import Platform
from card.core.error.lobby import CoolpadError,HolyTreeError

from card.lobby.aop.logging import trace_service
from card.lobby.apps.holytree.backends import BaseBackend
from card.lobby.apps.holytree import models as holytree_models
from card.lobby.apps.player import models as player_models

from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.coolpad.models import Coolpad


@go.logging.class_wrapper
class CoolpadBackend(BaseBackend):

    def _login(self, authorization_code):
        grant_type = 'authorization_code'
        client_id = settings.COOLPAD.app_id
        client_secret = settings.COOLPAD.app_key
        code = authorization_code
        redirect_uri = settings.COOLPAD.app_key
        massege="grant_type={0}&client_id={1}&client_secret={2}&code={3}&redirect_uri={4}".format(grant_type,client_id,client_secret,code,redirect_uri)

        login_url = settings.COOLPAD.login_url+'?'+massege
        resp = requests.get(login_url)
        if resp is None or resp == "" or resp.content is None or resp.content == "":
            return
        '''
        result = json.loads(resp.content.decode('string-escape').strip('"'))

        recode = result["ResultCode"]
        recontent = result['Content']
        resign = result['Sign']
        sign = hashlib.md5(app_id + str(recode) + urllib.unquote(recontent) + secret_key).hexdigest()
        if recode != 1 or resign != sign or recontent is None or recontent == "":
            raise CoolpadError.AUTH_FAILED(token=sessionid, code=recode)
            return

        content = urllib.unquote(recontent)
        content = base64.b64decode(content)
        content = ujson.loads(content)
        '''
        json_resp=ujson.loads(resp.content)
        #coolpad_user_id = json_resp['openid']
        #access_token = json_resp['access_token']
        #open_id = json_resp['open_id']
        #self.logger.debug(" [uid|%s]",  coolpad_user_id)
        return json_resp

    @trace_service
    def authenticate(self,sessionId, device_name, device_id, device_model,os_version, os_platform, app_version, channel, vender, login_ip, package_type,service_repositories, activity_repository, counter_repository, need_creation, **_):
        if channel != settings.COOLPAD.channel:
            raise TypeError("channel wrong")
        self.logger.debug("[session|%s]", sessionId)
        incompatible_versions = settings.HOLYTREE.incompatible_versions
        if (package_type in incompatible_versions and
            app_version in incompatible_versions[package_type]):
            raise HolyTreeError.incompatible_version()

        super(CoolpadBackend, self).authenticate(package_type, device_id, app_version)

        auth_resp = None

        auth_resp = self._login(sessionId)
        if auth_resp is None:
            return
        uid = int(auth_resp['openid'])
        access_token = auth_resp['access_token']
        assert uid is not None
        try:
            coolpad = Coolpad.get_coolpad_by_uid(uid=uid)
            user_id = coolpad.user_id
        except CoolpadError.UID_NOT_EXIST:
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
        re = redis.Redis(**settings.PERSIST_REDIS)
        coolpad_token={'openid':uid,'access_token':access_token}
        re.setex(user_id, ujson.dumps(coolpad_token), 2592000)
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

        self.logger.debug('coolpad [user_id|%s] [device_id|%s] [login_ip|%s]'
                '[uid|%s] [app_version|%s] [device_name|%s] authenticate successed',
                 user_id, device_id, login_ip, uid, app_version, device_name)
        #self._reset_fetch_time(user_id, service_repositories, activity_repository)

        return player

    def create_new_player(self, uid, device_id, nick_name, app_version,
                          channel, vender, login_ip, package_type, os_version, os_platform,
                          service_repositories, activity_repository):
        holytree_models.CreatePolicy.create_account("coolpad" + str(uid))
        try:
            player = super(CoolpadBackend, self).create_new_player(
                        device_id, nick_name, Platform.BAIDU, channel, vender,
                        app_version, os_version, os_platform, login_ip, package_type,
                        service_repositories, activity_repository)

            ly = Coolpad()
            ly.player = player
            ly.uid = uid
            ly.save()
        except Exception:
            holytree_models.CreatePolicy.delete_account("coolpad" + str(uid))
            raise

        return player.user_id
