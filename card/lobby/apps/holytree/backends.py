import time
import traceback
import hashlib
import base64
import urllib
import datetime
import ujson
from Crypto.Cipher import AES

import go.logging
from go.util import DotDict
from go.error import Error, Warning
from go.containers import redis
from go.containers.containers import Hash, Set
from card.api.task.timeline_service import TimelineService as MailService
from card.core.enum import Vip
from card.core.util.timestamp import get_timestamp_for_now
from card.core.conf import settings
from card.core.enum import Gender, Platform
from card.core.error.lobby import HolyTreeError

from card.lobby.aop.logging import trace_service
from card.lobby.extensions.logging import mongo_logger
from card.lobby.apps.player import models as player_models
from card.lobby.apps.holytree import models as holytree_models
from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.activity.base import ActivityHandler
from card.lobby.apps.timeline.service import TimeLineService
from card.lobby.apps.task.service import TaskService
from card.lobby.apps.store.models import PlayerProperty
from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.holytree.service import HolyTreeService

@go.logging.class_wrapper
class BaseBackend(object):

    def _net_prefix(self, ip_adress, prefix_count):
        ip_net_list = ip_adress.split(".")[:prefix_count]
        ip_net = ".".join(ip_net_list)
        return ip_net

    def _login_ip_count_limitation(self, user_id, ip_prefix, hash_key, max_count, ttl):
        re = redis.Redis(**settings.PERSIST_REDIS)
        need_set_expire = False
        if not re.exists(hash_key):
            need_set_expire = True

        ip_hash = Hash(hash_key, re)
        json_value = ip_hash.hget(ip_prefix)
        if json_value is not None:
            user_ids = ujson.loads(json_value)
        else:
            user_ids = []
        if user_id in user_ids:
            return

        if len(user_ids) > max_count:
            raise HolyTreeError.IP_CREATE_FREQUENTLY(ip_address="login_ip_count_limitation:" + ip_prefix)

        user_ids.append(user_id)
        ip_hash.hset(ip_prefix, ujson.dumps(user_ids))

        if need_set_expire:
            re.expire(hash_key, ttl)

    def _login_black_ip_limitation(self, login_ip):
        cfg = settings.HOLYTREE.login_ip_limitation.black_ip
        if not cfg.active:
            return
        re_persist = redis.Redis(**settings.PERSIST_REDIS)
        black_ips = Set(cfg.black_ip_set_key, re_persist)
        for ip_prefix in black_ips:
            if login_ip.startswith(ip_prefix):
                raise HolyTreeError.IP_LOGON_FREQUENTLY(ip_address="logon_ip_black_list_limit:" + login_ip)

    def _login_ip_check(self, user_id, login_ip, service_repositories, activity_repository):
        self._login_black_ip_limitation(login_ip)

        player_service = PlayerService(service_repositories, activity_repository)
        profile = player_service.get_profile(user_id)
        if profile.vip_title >= Vip.CROWN:
            return

        #only for the abnormal player for frienquent limit
        re = redis.Redis(**settings.PERSIST_REDIS)
        no_daily_award_ids = Set(settings.PLAYER.abmormal_player_set, re)
        if user_id not in no_daily_award_ids:
            return

        today = datetime.date.today()
        ip_cfg = settings.HOLYTREE.login_ip_limitation.ip_adress
        net_cfg = settings.HOLYTREE.login_ip_limitation.ip_net

        if ip_cfg.active:
            ip_key = ip_cfg.hash_key.format(today)
            ip_ttl = ip_cfg.ttl
            ip_max_count = ip_cfg.max_count
            self._login_ip_count_limitation(user_id, login_ip, ip_key, ip_max_count, ip_ttl)

        if net_cfg.active:
            net_key = net_cfg.hash_key.format(today)
            net_ttl = net_cfg.ttl
            net_max_count = net_cfg.max_count
            ip_net = self._net_prefix(login_ip, net_cfg.prefix_count)
            self._login_ip_count_limitation(user_id, ip_net, net_key, net_max_count, net_ttl)

    def _create_ip_count_limit(self, create_ip):
        cfg = settings.HOLYTREE.create_ip_limition.ip_count
        today = datetime.date.today()
        now = datetime.datetime.now()

        if not cfg.active:
            return

        assert cfg.start_hour <= cfg.end_hour
        if cfg.start_hour < cfg.end_hour:
            if now.hour < cfg.start_hour or now.hour > cfg.end_hour:
                return
        else:
            if now.hour != cfg.start_hour:
                return

        re = redis.Redis(**settings.PERSIST_REDIS)
        key = cfg.ip_hash_key.format(today)

        need_set_expire = False
        if not re.exists(key):
            need_set_expire = True

        ip_hash = Hash(key, re)
        ip_net = self._net_prefix(create_ip, cfg.prefix_count)
        json_value = ip_hash.hget(ip_net)
        create_count = 0 if json_value is None else int(json_value)

        if create_count >= cfg.max_ip_create_count:
            raise HolyTreeError.IP_CREATE_FREQUENTLY(ip_address="create_ip_count_limit:" + ip_net)
        ip_hash.hset(ip_net, create_count + 1)

        if need_set_expire:
            re.expire(key, cfg.ip_hash_key_expire)

    def _create_ip_frequent_limit(self, create_ip):
        cfg = settings.HOLYTREE.create_ip_limition.ip_frequency
        if not cfg.active:
            return

        re = go.containers.get_client()
        key = cfg.create_ip_prefix.format(create_ip)
        if re.exists(key):
             raise HolyTreeError.IP_CREATE_FREQUENTLY(ip_address="create_ip_frequent_limit:" + create_ip)
        else:
            expire_time = time.time() + cfg.interval
            re.setex(key, expire_time, cfg.interval)

    def _create_ip_black_list_limit(self, create_ip):
        cfg = settings.HOLYTREE.create_ip_limition.black_ip
        if not cfg.active:
            return
        re_persist = redis.Redis(**settings.PERSIST_REDIS)
        black_ips = Set(cfg.black_ip_set_key, re_persist)
        for ip_prefix in black_ips:
            if create_ip.startswith(ip_prefix):
                raise HolyTreeError.IP_CREATE_FREQUENTLY(ip_address="create_ip_black_list_limit:" + create_ip)

    def _create_ip_check(self, create_ip):
        self._create_ip_black_list_limit(create_ip)
        self._create_ip_frequent_limit(create_ip)
        self._create_ip_count_limit(create_ip)

    def _is_white_create_device_id(self, device_id):
        cfg = settings.HOLYTREE.create_device_limition.white_device
        if not cfg.active:
            return False
        re = redis.Redis(**settings.PERSIST_REDIS)
        device_id_set = Set(cfg.device_set_key, re)
        if device_id in device_id_set:
            return True
        else:
            return False

    def _create_device_count_limitation(self, package_type, device_id):
        cfg = settings.HOLYTREE.create_device_limition.device_count
        if not cfg.active:
            return
        create_count = self._device_account_count(package_type, device_id)
        if create_count >= cfg.device_create_count:
            raise HolyTreeError.DEVICE_CREATE_TOO_MUCH(device_id=device_id)

    def _create_device_check(self, package_type, device_id):
        if self._is_white_create_device_id(device_id):
            return
        self._create_device_count_limitation(package_type, device_id)

    def _create_version_limitation(self, package_type, app_version):
        cfg = settings.HOLYTREE.version_limition
        if not cfg.active:
            return
        if app_version in cfg.disable_versions:
            raise HolyTreeError.DISABLED_VERSION()

    def _device_account_count(self, package_type, device_id):
        cfg = settings.HOLYTREE.create_device_limition.device_count
        re = redis.Redis(**settings.PERSIST_REDIS)
        key = cfg.create_device_key
        create_hash = Hash(key, re)
        value = create_hash.hget(device_id)
        return int(value) if value is not None else 0

    def _incr_create_count(self, package_type, device_id):
        cfg = settings.HOLYTREE.create_device_limition.device_count
        re = redis.Redis(**settings.PERSIST_REDIS)
        key = cfg.create_device_key
        create_hash = Hash(key, re)
        create_hash.hincrby(device_id, 1)

    def _reset_timeline_time(self, user_id, service_repositories, activity_repository):
        timeline_service = TimeLineService(service_repositories,  activity_repository)
        timeline_service.reset_fetch_time(user_id)
        timeline_service.reset_ttl_time(user_id)

    def _send_create_message(self, user_id, service_repositories, activity_repository):
        login_greet = settings.TIME_LINE.personal_messages.register_greet
        timeline_service = TimeLineService(service_repositories, activity_repository)
        timeline_service.send_personal_message(user_id, login_greet)

    def _exclude_suffix(self, string):
        lower_string = string.lower()
        for suffix in settings.HOLYTREE.exclude_suffixs:
            if lower_string.endswith(suffix.lower()):
                return lower_string[:-len(suffix)]
        return lower_string

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

    def authenticate(self, package_type, device_id, app_version):
        incompatible_versions = settings.HOLYTREE.incompatible_versions
        if (package_type in incompatible_versions and
            app_version in incompatible_versions[package_type]):
            raise HolyTreeError.INCOMPATIBLE_VERSION()

        re = redis.Redis(**settings.PERSIST_REDIS)
        key = settings.HOLYTREE.deactived_device_set_key
        deactived_devices = Set(key, re)
        if device_id in deactived_devices:
            raise HolyTreeError.DEVICE_DEACTIVED(device_id=device_id)

    def create_new_player(self, device_id, nick_name, player_type, channel,
                          vender, app_version, os_version, os_platform, login_ip,
                          package_type, service_repositories, activity_repository):
        self._create_version_limitation(package_type, app_version)
        self._create_device_check(package_type, device_id)
        self._create_ip_check(login_ip)

        player = player_models.Player()
        player.nick_name = self._exclude_suffix(nick_name)
        player.gender = Gender.UNKNOWN
        player.avatar_url = '5'
        player.channel = channel
        player.save()

        #nickname for android's newer
        new_nick_name = player.nick_name + str(player.user_id)[-4:]
        player.nick_name = new_nick_name
        player.save()

        property = PlayerProperty()
        property.player = player
        property.name_card = 1
        property.save()

        profile = player_models.PlayerProfile()
        profile.player = player
        profile.save()

        player_extra = player_models.PlayerExtra()
        player_extra.player = player
        player_extra.player_type = player_type
        player_extra.app_version = app_version
        player_extra.os_version = os_version
        player_extra.os_platform = os_platform
        player_extra.created_device_id = device_id
        player_extra.channel = channel
        player_extra.bank_password = hashlib.md5("123456").hexdigest()
        player_extra.save()

        three = player_models.PlayerThree()
        three.player = player
        three.save()

        fruit = player_models.PlayerFruit()
        fruit.player = player
        fruit.save()

        #player should not get the update award 
        #when it creates account on the version!
        re = redis.Redis(**settings.PERSIST_REDIS)
        status_hash = Hash(settings.ACTIVITY.updated_player_key.format(player.user_id), db=re)
        status_hash.hset(player.user_id, app_version)

        #if more than one account create on one device, only first account 
        #can draw the bind account award, so if it is not the first account
        #make task status to "has drawed"
        #if self._device_account_count(package_type, device_id):
            #give counter_repository None to avoid forward many argument.
            #and currently, we do not use the counter_repository for the function
        #    task_service = TaskService(service_repositories, activity_repository, None)
        #    task_service.update_award_status(player.user_id, 17, awarded=True)

        self._incr_create_count(package_type, device_id)
        self._send_create_message(player.user_id, service_repositories, activity_repository)
        ActivityHandler.process_register(user_id=player.user_id, 
                                    activity_repository=activity_repository, 
                                    service_repositories=service_repositories, 
                                    context=DotDict({'device_id':device_id}))
        mongo_logger.player_register(
            user_id=player.user_id, nick_name=nick_name,
            player_type=player_type, app_version=app_version,
            os_version=os_version, os_platform=os_platform,
            device_id=device_id, channel=channel, vender=vender,
            login_ip=login_ip, timestamp=get_timestamp_for_now(unit='ms')
        )

        return player

    def get_user(self, user_id):
        player = None
        try:
            player = player_models.SessionPlayer(user_id)
        except Exception as e:
            self.logger.error(e.message)
            traceback.print_exc()
        finally:
            return player

@go.logging.class_wrapper
class GuestBackend(BaseBackend):

    def authenticate(self, device_id, device_name, app_version, channel,
                     vender, login_ip, os_version, os_platform, package_type,
                     service_repositories, activity_repository, **_):
        super(GuestBackend, self).authenticate(package_type, device_id, app_version)

        try:
            guest = holytree_models.Guest.get_guest_by_device_id(device_id=device_id)
            user_id = guest.user_id
        except HolyTreeError.USER_NAME_NOT_EXIST:
            user_id = self.create_new_player(
                device_id=device_id, device_name=device_name,
                app_version=app_version, channel=channel, vender=vender,
                os_version=os_version, os_platform=os_platform,
                login_ip=login_ip, package_type=package_type,
                service_repositories=service_repositories, 
                activity_repository=activity_repository)

        try:
            service = PlayerService(service_repositories, activity_repository)
            service.login(user_id)
            player = player_models.SessionPlayer(user_id)
        except Error as e:
            self.logger.error(e.message)
            traceback.print_exc()
            raise
        except Warning as e:
            self.logger.warn(e.message)
            raise
        except Exception as e:
            self.logger.error(e.message)
            traceback.print_exc()
            return None
        self.logger.debug('[user_id|%s] [device_id|%s] [app_version|%s] [device_name|%s] '
                          'authenticate successed', user_id, device_id, app_version, device_name)
        self._reset_timeline_time(user_id, service_repositories, activity_repository)
        return player

    def create_new_player(self, device_id, device_name, app_version, 
                          channel, vender, login_ip, package_type, os_version, os_platform,
                          service_repositories, activity_repository):
        holytree_models.CreatePolicy.create_account(device_id)
        try:
            player = super(GuestBackend, self).create_new_player(
                        device_id, device_name, Platform.GUEST, channel, vender,
                        app_version, os_version, os_platform, login_ip, package_type,
                        service_repositories, activity_repository)
            
            guest = holytree_models.Guest()
            guest.player = player
            guest.device_id = device_id
            guest.save()
        except Exception:
            holytree_models.CreatePolicy.delete_account(device_id)
            raise

        return player.user_id

@go.logging.class_wrapper
class RobotBackend(object):

    def authenticate(self, user_id, token, service_repositories, activity_repository):
        user_id = int(user_id)
        self.logger.info('[robot|%d][token|%s] login', user_id, token)
        if user_id is None or token is None:
            return None

        try:
            robot = holytree_models.Robot.objects.get(player__user_id=user_id)
            if robot.token == token:
                service = PlayerService(service_repositories,
                                        activity_repository)
                service.login(user_id)
                player = player_models.SessionPlayer(user_id)
                return player
            else:
                self.logger.debug('[robot|%d][login_token|%s] != [token|%s]',
                                  user_id, token, robot.token)
                return None
        except holytree_models.Robot.DoesNotExist:
            self.logger.debug('[robot|%d] not exist', user_id)
            return None

    def get_user(self, player_id):
        robot = player_models.SessionPlayer(user_id=player_id)
        return robot

@go.logging.class_wrapper
class HolyTreeBackend(BaseBackend):

    @trace_service
    def authenticate(self, user_name, password, device_name, device_id, device_model, 
                    os_version, os_platform, app_version, channel, vender, login_ip, package_type,
                    service_repositories, activity_repository, counter_repository, need_creation, **_):
        super(HolyTreeBackend, self).authenticate(package_type, device_id, app_version)
        user_name = user_name.strip()
        user_name = user_name.lower()
        password = self._decode_password(user_name, app_version, password)

        try:
            holytree = holytree_models.HolyTree.get_holytree_by_user_name(user_name=user_name)
        except HolyTreeError.USER_NAME_NOT_EXIST:
            if not need_creation:
                raise
            self.create_new_player(user_name, password, device_name, device_id, 
                device_model, os_version, os_platform, app_version, channel, vender, 
                login_ip, package_type, service_repositories, activity_repository, counter_repository)
            if int(app_version.replace('.','')) >= 200:
                return
            else:
                holytree = holytree_models.HolyTree.get_holytree_by_user_name(user_name=user_name)
        except Exception as ex:
            self.logger.error(ex.message)
            traceback.print_exc()
            raise
        else:
            if need_creation:
                raise HolyTreeError.USER_NAME_ALREADY_EXIST(user_name=user_name)

        user_id = holytree.user_id
        encodered_pwd = hashlib.md5(password).hexdigest()
        if encodered_pwd != holytree.password:
            raise HolyTreeError.AUTH_FAILED(user_name=user_name, password=encodered_pwd)

        try:
            player_service = PlayerService(service_repositories, activity_repository)
            player_service.login(user_id)
        except Error as e:
            self.logger.error(e.message)
            raise
        except Warning as e:
            self.logger.warn(e.message)
            raise
            
        player = player_models.SessionPlayer(user_id)
        self.logger.debug('holytree [user_id|%s] [user_name|%s] [device_id|%s] [login_ip|%s]'
                '[app_version|%s] [device_name|%s] authenticate successed',
                user_id, user_name, device_id, login_ip, app_version, device_name)
        
        self._reset_timeline_time(user_id, service_repositories, activity_repository)
        return player
    def create_new_player(self, user_name, password, device_name,
                        device_id, device_model, os_version, os_platform,
                        app_version, channel, vender, login_ip, package_type,
                        service_repositories, activity_repository, counter_repository):
        if int(app_version.replace('.','')) >= 200:
            session_info = {}
            session_info["user_name"] = user_name
            session_info["device_name"] = device_name
            session_info["password"] = password
            session_info["device_id"] = device_id
            session_info["device_model"] = device_model
            session_info["os_version"] = os_version
            session_info["os_platform"] = os_platform
            session_info["app_version"] = app_version
            session_info["channel"] = channel
            session_info["vender"] = vender
            session_info["login_ip"] = login_ip
            session_info["package_type"] = package_type
            session_info["temp"] = 0
            player = super(HolyTreeBackend, self).create_new_player(
                            device_id, device_name, Platform.HOLYTREE, channel, vender,
                            app_version, os_version, os_platform, login_ip, package_type,
                            service_repositories, activity_repository)
            user_id=player.user_id
            session_info['user_id']=user_id
            self.send_email(user_name, session_info, type='regist')
            for counter in counter_repository.counters:
                counter.incr(player.user_id, **{'bind_account':1})
        else:
            holytree_models.CreatePolicy.create_account(user_name)
            try:
                player = super(HolyTreeBackend, self).create_new_player(
                            device_id, device_name, Platform.HOLYTREE, channel, vender,
                            app_version, os_version, os_platform, login_ip, package_type,
                            service_repositories, activity_repository)

                holytree = holytree_models.HolyTree()
                holytree.player = player
                holytree.user_name = user_name
                holytree.password = hashlib.md5(password).hexdigest()
                holytree.save()
            except Exception:
                holytree_models.CreatePolicy.delete_account(user_name)
                raise

            '''
            holytree_models.CreatePolicy.create_account(user_name)
            try:
                player = super(HolyTreeBackend, self).create_new_player(
                            device_id, device_name, Platform.HOLYTREE, channel, vender,
                            app_version, os_version, os_platform, login_ip, package_type,
                            service_repositories, activity_repository)
                re = redis.Redis(**settings.PERSIST_REDIS)
                session_info = {}
                session_info["user_name"] = user_name
                session_info["password"] = password
                re.setex('regist', ujson.dumps(session_info), settings.HOLYTREE.check_email.token_expire_time)
                re.setex('player', player, settings.HOLYTREE.check_email.token_expire_time)
                self.send_email(user_name,password,type='regist')
                holytree = holytree_models.HolyTree()
                holytree.player = player
                holytree.user_name = user_name
                holytree.password = hashlib.md5(password).hexdigest()
                holytree.save()
            except Exception:
                holytree_models.CreatePolicy.delete_account(user_name)
                raise
            for counter in counter_repository.counters:
                counter.incr(player.user_id, **{'bind_account':1})
            '''
        
    def check_email(self,token,service_repositories,activity_repository,counter_repository):
        re = redis.Redis(**settings.PERSIST_REDIS)
        if not re.exists(token):
            return 0
        data = re.get(token)
        data = ujson.loads(data)
        user_name=data['user_name']
        device_name=data['device_name']
        password=data['password']
        device_id=data['device_id']
        device_mode=data['device_model']
        os_version=data['os_version']
        os_platform=data['os_platform']
        app_version=data['app_version']
        channel=data['channel']
        vender=data['vender']
        login_ip=data['login_ip']
        package_type=data['package_type']
        temp = data ["temp"]
        user_id=data["user_id"]
        holytree_models.CreatePolicy.create_account(user_name)
        if temp==0:
            try:
                player = player_models.Player.get_player(user_id)
                holytree = holytree_models.HolyTree()
                holytree.player = player
                holytree.user_name = user_name
                holytree.password = hashlib.md5(password).hexdigest()
                try:
                    holytree.save()
                except Exception as ex:
                    print ex
                    return
            except Exception:
                holytree_models.CreatePolicy.delete_account(user_name)
                return 0
            data['temp'] = 1
            re.setex(token, ujson.dumps(data), settings.HOLYTREE.check_email.token_expire_time)
            for counter in counter_repository.counters:
                counter.incr(player.user_id, **{'bind_account': 1})
            return 1
        else:
            return 0

    def _send_check_email(self, user_mail, token, type):
        subject = settings.HOLYTREE.check_email.subject
        data = '{"user_mail":"%s","token":"%s","type":"%s"}' % (user_mail,token,type)
        parameter = base64.b64encode(data)
        url = settings.HOLYTREE.check_email.url_prefix.format(parameter)
        context = settings.HOLYTREE.check_email.context.format(url)
        mail_service = MailService()
        mail_service.send_mail(subject, context, user_mail)

    def send_email(self, user_email, session_info, type):
        # user=self.check_token(user_email)
        token = settings.HOLYTREE.check_email.token_key_prefix.format(user_email, time.time())
        token = token.strip()
        encoded_token = hashlib.md5(token).hexdigest().upper()
        re = redis.Redis(**settings.PERSIST_REDIS)
        re.setex(encoded_token, ujson.dumps(session_info), settings.HOLYTREE.check_email.token_expire_time)
        self._send_check_email(user_email, encoded_token, type)

'''
    def create_new_player(self, user_name, password, device_name, 
                        device_id, device_model, os_version, os_platform, 
                        app_version, channel, vender, login_ip, package_type,
                        service_repositories, activity_repository, counter_repository):
        holytree_models.CreatePolicy.create_account(user_name)
        try:
            player = super(HolyTreeBackend, self).create_new_player(
                        device_id, device_name, Platform.HOLYTREE, channel, vender,
                        app_version, os_version, os_platform, login_ip, package_type,
                        service_repositories, activity_repository)
            holytree_service = HolyTreeService(service_repositories,activity_repository, counter_repository)
            user_id=player.user_id
            holytree_service.send_email(int(user_id), user_name, password,type="regist")
            re = redis.Redis(**settings.PERSIST_REDIS)
            session_info = {}
            session_info["user_name"] = user_name
            session_info["device_name"] = device_name
            session_info["password"] = password
            session_info["device_id"] = device_id
            session_info["device_model"] = device_model
            session_info["os_version"] = os_version
            session_info["os_platform"] = os_platform
            session_info["app_version"] = app_version
            session_info["channel"] = channel
            session_info["vender"] = vender
            session_info["login_ip"] = login_ip
            session_info["package_type"] = package_type
            session_info["service_repositories"] = service_repositories
            session_info["activity_repository"] = activity_repository
            session_info["counter_repository"] = counter_repository
            re.setex('regist', ujson.dumps(session_info), settings.HOLYTREE.check_email.token_expire_time)
            #holytree = holytree_models.HolyTree()
            #holytree.user_name = user_name
            #holytree.password = hashlib.md5(password).hexdigest()
            #holytree.save()
        except Exception:
            holytree_models.CreatePolicy.delete_account(user_name)
            raise
        for counter in counter_repository.counters:
            counter.incr(player.user_id, **{'bind_account':1})
'''
