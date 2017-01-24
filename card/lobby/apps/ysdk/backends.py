__all__ = ['YsdkBackend']

import time
import hashlib
import urllib
import urlparse
import thread
import ujson
import requests
import base64
import json
import urllib2
import urlparse
import traceback
from requests.exceptions import RequestException
from xml.etree import ElementTree 

from go.util import DotDict
import go.logging
from go.error import Error, Warning

from card.core.conf import settings
from card.core.enum import Platform
from card.core.error.lobby import YsdkError,HolyTreeError

from card.lobby.aop.logging import trace_service
from card.lobby.apps.holytree.backends import BaseBackend
from card.lobby.apps.holytree import models as holytree_models
from card.lobby.apps.player import models as player_models
from card.lobby.apps.player.models import SessionPlayer
from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.ysdk.models import Ysdk
from card.lobby.apps.ysdk.service import YsdkService
from card.lobby.pool import ysdk_session_pool

@go.logging.class_wrapper
class YsdkBackend(BaseBackend):

    def _login(self, account_type, open_id, open_key, user_ip):
        app_id = settings.YSDK.qq_app_id
        app_key = settings.YSDK.qq_app_key
        login_url = settings.YSDK.qq_login_url
        if account_type == '2':
            login_url = settings.YSDK.wx_login_url
            app_id = settings.YSDK.wx_app_id
            app_key = settings.YSDK.wx_app_key
        timestamp = int(time.time())
        sign = hashlib.md5(str(app_key) + str(timestamp)).hexdigest()
        request_body={
            'appid':app_id,
            'openid':open_id,
            'openkey':open_key,
            'userip':user_ip,
            'sig':sign,
            'timestamp':timestamp,
        }

        url = login_url + '?'
        first = True
        for v in request_body:
            if first:
                first = False
            else:
                url += '&'
            url += v + '=' + str(request_body[v])
        resp = requests.get(url)
        if resp is None or resp == "" or resp.content is None or resp.content == "":
            return
        result = json.loads(resp.content.decode('string-escape').strip('"'))
        recode = result["ret"]
        if recode != 0:
            raise YsdkError.AUTH_FAILED(account_type=account_type, open_id=open_id, open_key=open_key, code=recode)
        return open_id

    @trace_service
    def authenticate(self, account_type, open_id, open_key, device_name, device_id, device_model, 
                    os_version, os_platform, app_version, channel, vender, login_ip, package_type,
                    service_repositories, activity_repository, counter_repository, **_):
        uid=open_id
        self.logger.debug("[open_id|%s]", uid)
        incompatible_versions = settings.HOLYTREE.incompatible_versions
        if (package_type in incompatible_versions and
            app_version in incompatible_versions[package_type]):
            raise HolyTreeError.INCOMPATIBLE_VERSION()
        
        super(YsdkBackend, self).authenticate(package_type, device_id, app_version)
        
        auth_resp = None
        if settings.YSDK.need_auth:
            auth_resp = self._login(account_type, uid, open_key, login_ip)
            if auth_resp is None:
                return
            uid = auth_resp
            assert uid is not None

        try:
            ysdk = Ysdk.get_ysdk_by_open_id(open_id=uid)
            user_id = ysdk.user_id
        except YsdkError.OPEN_ID_NOT_EXIST:
            self.logger.debug('[uid|%s] [device_id|%s] '
                '[app_version|%s] [device_name|%s] first login, now create',
                uid, device_id, app_version, device_name)
            nick_name = device_name + str(uid)[-4:]
            user_id = self.create_new_player(uid, open_key, "", account_type, device_id, nick_name, app_version, 
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

        self.logger.debug('ysdk [user_id|%s] [device_id|%s] [login_ip|%s]'
                '[uid|%s] [app_version|%s] [device_name|%s] authenticate successed',
                 user_id, device_id, login_ip, uid, app_version, device_name)
        #self._reset_fetch_time(user_id, service_repositories, activity_repository)

        return player

    def create_new_player(self, uid, open_key, pf, account_type,
            device_id, nick_name, app_version, 
                          channel, vender, login_ip, package_type, os_version, os_platform,
                          service_repositories, activity_repository):
        holytree_models.CreatePolicy.create_account("ysdk" + str(uid))
        try:
            player = super(YsdkBackend, self).create_new_player( 
                        device_id, nick_name, Platform.YSDK, channel, vender,
                        app_version, os_version, os_platform, login_ip, package_type,
                        service_repositories, activity_repository)
            
            ly = Ysdk()
            ly.player = player
            ly.open_id = uid
            ly.open_key=open_key
            ly.pf=pf
            ly.account_type=account_type
            ly.save()
        except Exception:
            holytree_models.CreatePolicy.delete_account("ysdk" + str(uid))
            raise

        return player.user_id
