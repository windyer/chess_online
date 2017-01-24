__all__ = ['IapppayBackend']

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
from card.core.error.lobby.iapppay_error import IApppayError

from card.lobby.aop.logging import trace_service
from card.lobby.apps.holytree.backends import BaseBackend
from card.lobby.apps.holytree import models as holytree_models
from card.lobby.apps.player import models as player_models
from card.lobby.apps.player.models import SessionPlayer
from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.iapppay.models import Iapppay
from card.lobby.pool import iapppay_session_pool
from Crypto.PublicKey import RSA
from card.lobby.apps.iapppay.crypto import CryptoHelper

@go.logging.class_wrapper
class IapppayBackend(BaseBackend):

    crypto = None
    privateKey = None
    platpkey = None

    def _init_key(self):
        if IapppayBackend.crypto is None:
            IapppayBackend.crypto = CryptoHelper()
            IapppayBackend.privateKey = CryptoHelper.importKey(settings.IAPPPAY.zx010_appvkey)
            IapppayBackend.platpkey = CryptoHelper.importKey(settings.IAPPPAY.zx010_platpkey)

    def _login(self, token):
        
        self._init_key()

        app_id = settings.IAPPPAY.zx010_app_id
        transdata = {"appid":app_id,"logintoken":token}
        req_text = ujson.dumps(transdata, ensure_ascii=False)
        sign = IapppayBackend.crypto.sign(req_text, IapppayBackend.privateKey)  
        request_body={
            'transdata':req_text,
            'sign':sign,
            'signtype':'RSA',
        }
        login_url = settings.IAPPPAY.login_url
        resp = requests.post(login_url, data=request_body)
        text = resp.content
        reqData = urllib.unquote(str(text)).decode('utf8')
        decoded_data = urlparse.parse_qs(reqData)

        transdata = decoded_data["transdata"][0]
        transdata = ujson.loads(transdata)
        if "code" in transdata:
            raise IApppayError.LOGIN_AUTH_FAILED(transdata=transdata, token=token)

        ok = IapppayBackend.crypto.segmentation_data(reqData, IapppayBackend.platpkey)
        if ok != True:
            raise IApppayError.AUTH_SIGN_LOGIN_FAILED(transdata=transdata) 

        return transdata['userid']

    @trace_service
    def authenticate(self, token, device_name, device_id, device_model, 
                    os_version, os_platform, app_version, channel, vender, login_ip, package_type,
                    service_repositories, activity_repository, counter_repository, **_):
        self.logger.debug("[token|%s]", token)
        incompatible_versions = settings.HOLYTREE.incompatible_versions
        if (package_type in incompatible_versions and
            app_version in incompatible_versions[package_type]):
            raise HolyTreeError.INCOMPATIBLE_VERSION()
        
        super(IapppayBackend, self).authenticate(package_type, device_id, app_version)
        
        auth_resp = None
        if settings.IAPPPAY.need_auth:
            auth_resp = self._login(token)
            if auth_resp is None:
                return
            uid = int(auth_resp)
            assert uid is not None

        try:
            iapppay = Iapppay.get_iapppay_by_uid(uid=uid)
            user_id = iapppay.user_id
        except IapppayError.UID_NOT_EXIST:
            self.logger.debug('[uid|%s] [device_id|%s] '
                '[app_version|%s] [device_name|%s] first login, now create',
                uid, device_id, app_version, device_name)
            nick_name = device_name + str(uid)[-4:]
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

        self.logger.debug('iapppay [user_id|%s] [device_id|%s] [login_ip|%s]'
                '[uid|%s] [app_version|%s] [device_name|%s] authenticate successed',
                 user_id, device_id, login_ip, uid, app_version, device_name)
        #self._reset_fetch_time(user_id, service_repositories, activity_repository)

        return player

    def create_new_player(self, uid, device_id, nick_name, app_version, 
                          channel, vender, login_ip, package_type, os_version, os_platform,
                          service_repositories, activity_repository):
        holytree_models.CreatePolicy.create_account("iapppay" + str(uid))
        try:
            player = super(IapppayBackend, self).create_new_player(
                        device_id, nick_name, Platform.IAPPPAY, channel, vender,
                        app_version, os_version, os_platform, login_ip, package_type,
                        service_repositories, activity_repository)
            
            ly = Iapppay()
            ly.player = player
            ly.uid = uid
            ly.save()
        except Exception:
            holytree_models.CreatePolicy.delete_account("iapppay" + str(uid))
            raise

        return player.user_id
