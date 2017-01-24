#coding=utf-8

import ujson
from datetime import date
import datetime
import copy
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response

from django.template.response import TemplateResponse
from django.contrib import messages
from django.conf import settings
import go.logging

from card.core.enum import Vip
from card.core.enum import Rank
from card.core.error.lobby import PlayerError
from card.core.enum import IdentifyType
from card.core.charge import ITEMS

from card.lobby.aop.logging import trace_view
from card.lobby.aop import request_limit, api_view_available
from card.lobby.settings import player,activity
from card.lobby import permissions
from card.lobby.apps.friend.service import FriendService
from card.lobby.apps.daily.service import DailyService
from card.lobby.apps.rank.service import RankService
from card.lobby.apps.freebie.service import FreebieService
from card.lobby.apps.activity.service import ActivityService
from card.lobby.apps.game.service import GameService
from card.lobby.apps.timeline.service import TimeLineService
from card.lobby.apps.task.service import TaskService
import card.lobby.apps.player.models as player_models
from card.lobby.apps.player import serializers
from card.lobby.apps.player.service import PlayerService, SensitiveFilter
from card.lobby.apps.store.redis import ChargeStatus
from card.lobby.apps.player.captcha_manager import CaptchaManager
from card.lobby.apps.player.idiom_manager import IdiomManager
from card.lobby.settings.player import MoneyBagType
from card.core.enum import Vip
from card.lobby.settings import activity
from card.lobby.extensions.logging.mongolog.mixin.channel_merge import channel_merge
@api_view(('GET',))
@api_view_available()
def api_view(request, format=None):
    return Response({
        'profile': reverse('profile-details', request=request, format=format),
        'refresh': reverse('refresh', request=request, format=format),
        'items': reverse('items', request=request, format=format),
        'deposit': reverse('deposit', request=request, format=format),
        'withdraw': reverse('withdraw', request=request, format=format),
        'bank_details': reverse('bank_details', request=request, format=format),
        'bank_password': reverse('bank_password', request=request, format=format),
        'bank_password/forget': reverse('forget-bank_password', request=request, format=format),
        'bank_password/reset': reverse('reset-bank_password', request=request, format=format),
        'update_avatar': reverse('update-avatar', request=request, format=format),
        'update_album': reverse('update-album', request=request, format=format),
        'delete_album': reverse('delete-album', request=request, format=format),
        'report_player': reverse('report-player', request=request, format=format),
        'identify_code': reverse('identify-code', request=request, format=format),
        'identify_idiom': reverse('identify-idiom', request=request, format=format),
        'vip_bag/draw': reverse('draw-vip-bag', request=request, format=format),
        'before': reverse('before', request=request, format=format),
        })

@go.logging.class_wrapper
class Items(generics.ListAPIView):

    serializer_class   = serializers.PropertyItem
    permission_classes = (permissions.IsPlayer,)
    paginate_by        = 20
    paginate_by_param  = 'page_size'

    def get_queryset(self):
        service   = PlayerService(self.request.service_repositories,
                                self.request.activity_repository)
        query_set = service.get_property_items(self.request.user.id)
        return query_set

    @trace_view
    def get(self, request, format=None):
        return super(Items, self).get(request, format)

def channel_bull_download(channel):
    channel_forbid_bull = ['88_zhiyifu_', '7012431',]
    for ch in channel_forbid_bull:
        if channel.find(ch) >= 0:
            return False
    return True

@go.logging.class_wrapper
class Refresh(generics.RetrieveAPIView):

    throttle_classes = (permissions.User5SecRateThrottle,)
    serializer_class = serializers.Refresh
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    def get(self, request, format=None):
        player_service = PlayerService(request.service_repositories,
                                request.activity_repository)
        game_service = GameService(request.service_repositories,
                                request.activity_repository)
        rank_service = RankService(request.service_repositories,
                                        request.activity_repository)
        timeline_service = TimeLineService(request.service_repositories,
                                request.activity_repository)
        task_service = TaskService(request.service_repositories,
                                request.activity_repository,
                                request.counter_repository)
        user_id = self.request.user.id
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        profile = player_service.get_profile(user_id)._asdict()
        profile['ranks'] = rank_service.get_user_ranks(user_id)
        profile['concurrent_users'] = game_service.get_concurrency()
        profile['unread_events'] = timeline_service.get_unread_info(user_id)
        profile['can_draw_task'] = task_service.can_draw_task(user_id)
        simple_channel = channel_merge(player_extra.channel)
        if  simple_channel in settings.PLAYER.online_configure.qmBZW['not_channel_bull_download']:
            profile['enable_bull_download'] = False
        else:
            profile['enable_bull_download'] = player.PLAYER.online_configure.qmBZW['enable_bull_download']
        profile['enable_activity'] = player.PLAYER.online_configure.qmBZW['enable_activity']
        profile["double_seventh_logo"] = activity.ACTIVITY['double_seventh']['double_seventh_logo']
        profile["double_seventh_discount"] = activity.ACTIVITY['double_seventh']['double_seventh_discount']
        if activity.ACTIVITY['double_seventh']['double_seventh_logo']:
            first_person = player_service.get_date_gift()
            profile["double_seventh"]={}
            profile["double_seventh"]=first_person
        if player_extra.app_version < settings.VIP.vip5_version:
            if profile['vip_title'] > Vip.CROWN:
                profile['vip_title'] = Vip.CROWN
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

@go.logging.class_wrapper
class ProfileDetails(generics.RetrieveAPIView,
                     generics.CreateAPIView):

    throttle_classes = (permissions.User5SecRateThrottle,)
    serializer_class = serializers.DetailProfile
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    def get(self, request, format=None, pk=None):
        user_id = self.request.user.id if pk is None else int(pk)

        player_service = PlayerService(request.service_repositories, request.activity_repository)
        daily_service = DailyService(request.service_repositories, request.activity_repository)
        rank_service = RankService(request.service_repositories, request.activity_repository)
        freebie_service = FreebieService(request.service_repositories, request.activity_repository)
        activity_service = ActivityService(request.service_repositories,
                            request.activity_repository, request.counter_repository)
        task_service = TaskService(request.service_repositories,
                                request.activity_repository,
                                request.counter_repository)

        profile = player_service.get_profile(user_id)._asdict()
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        profile.update(player_extra.attributes_dict)
        profile['property_items'] = player_service.get_property_items(user_id)
        profile['ranks'] = rank_service.get_user_ranks(user_id)
        profile['albums'] = player_service.get_albums(user_id, pk is None)
        profile["monthly_payment"] = player_extra.is_monthly_player
        if player_service.is_avatar_audit_pending(user_id):
            profile['avatar_url'] = '0'
        profile['signature'] = SensitiveFilter.filter(profile['signature'])
        profile['contact'] = SensitiveFilter.filter(profile['contact'])
        try:
            address = None
            geoip_resp = request.geoip_reader.city(player_extra.login_ip)
            if len(geoip_resp.subdivisions) and 'zh-CN' in geoip_resp.subdivisions[0].names:
                address = geoip_resp.subdivisions[0].names['zh-CN']
                if 'zh-CN' in geoip_resp.city.names:
                    address += geoip_resp.city.names['zh-CN']
            elif len(geoip_resp.subdivisions) and 'en' in geoip_resp.subdivisions[0].names:
                address = geoip_resp.subdivisions[0].names['en']
            if address is not None:
                profile['address'] = address
        except Exception:
            pass

        if pk is None:
            charge_status = ChargeStatus()
            yesterday = date.today() - datetime.timedelta(days=1)
            income_most_key = Rank.TODAY_INCOME_MOST.format(yesterday)
            profile['yesterday_top_players'] = rank_service.get_top_rank(income_most_key, 2)
            profile['yesterday_self_rank'] = rank_service.yesterday_win_rank(user_id)
            profile['month_statistic'] = player_service.get_month_statistic(user_id)
            profile['salvage_status'] = freebie_service.get_salvage_status(user_id)
            profile['money_tree_status'] = freebie_service.get_money_tree_status(user_id)
            profile['activity_status'] = activity_service.get_activity_status(user_id)
            profile['task_info'] = task_service.get_task_details(user_id)
            profile['daily_status'] = daily_service.get_daily_status(user_id,
                                        player_extra.continuous_login_days,
                                        profile['vip_title'], player_extra.login_device_id)
            profile['no_charge_items'] = charge_status.no_charge_items(user_id, profile["vip_title"],
                                                player_extra.package_type, player_extra.channel)
            profile["has_charged_coin"] = True
            profile["first_day_login"] = player_extra.first_time_login
            profile["monthly_payment_end_time"] = player_extra.monthly_payment_end_time
            profile["monthly_payment_available"] = settings.STORE.monthly_payment_available
            if profile["vip_title"] >= Vip.CROWN:
                request.session['is_identified'] = True
            if player_extra.app_version < settings.VIP.vip5_version:
                if profile['vip_title'] > Vip.CROWN:
                    profile['vip_title'] = Vip.CROWN
            profile['is_identified'] = request.session['is_identified']
            profile["identify_type"] = request.session["identify_type"]
            if not profile['is_identified'] and request.session["identify_type"] == IdentifyType.NUMBER:
                captcha_manager = CaptchaManager()
                (code, image_url) = captcha_manager.generator_image(user_id)
                request.session["code"] = code
                profile["identify_image_url"] = image_url
            elif not profile['is_identified'] and request.session["identify_type"] == IdentifyType.IDIOM:
                idiom_manager = IdiomManager()
                code, idiom = idiom_manager.random_idiom()
                request.session["code"] = idiom
                profile["idiom_code"] = code

            if player_extra.package_type in settings.PLAYER.online_configure:
                profile["online_configure"] = copy.deepcopy(settings.PLAYER.online_configure[player_extra.package_type])

                profile["online_configure"]["cat_cash_factor"] = settings.CATFOOD.cash_factor
                profile["online_configure"]["cat_turn_weight"] = settings.CATFOOD.turn_weight
                profile["online_configure"]["cat_min_weight"] = settings.CATFOOD.min_cat_weight
                if player_extra.app_version >= "1.7.0":
                    profile["online_configure"]["enable_daily_charge_award"] = True
                else:
                    profile["online_configure"]["enable_daily_charge_award"] = False
                for app in settings.ZHUOYI.app_conf:
                    if player_extra.channel in settings.ZHUOYI.app_conf[app].channels:
                        profile["online_configure"]['mall_money_bag_type'] = MoneyBagType.NEWYEAR_SIX_RMB_BAGS
                    else:
                        profile["online_configure"]['mall_money_bag_type'] = MoneyBagType.MONKEY_FIFTY_RMB_BAGS

            profile["next_online_award_step"] = daily_service.get_next_online_award_step(user_id)
            profile["created_days"] = player_extra.created_days
            profile["max_cat_weight"] = settings.PLAYER.max_cat_weight
            profile["newbie_item"] = ITEMS.coins[settings.STORE.lobby_newbie_item]
            profile["newbie_item"]["item_id"] = settings.STORE.lobby_newbie_item.item_id
            profile['limited_item'] = charge_status.limited_item_end_time(user_id)
            profile['limited_item_buy_count'] = charge_status.get_limited_item_buy_count(user_id)
            profile['highest_award'] = player_service.get_highest_award()
            profile['game_min_cash'] = player_service.get_game_min_cash()
            profile['bull_download_count'] = player_service.get_bull_download_count()
            profile["online_configure"]["charge_limit"] = player.PLAYER['charge_limit']
            profile["needUpdate"] = player.PLAYER['needUpdate']
            profile["update_url"] = player.PLAYER['update_url']
            profile["online_configure"]["all_chat"] = player.PLAYER['all_chat']
            profile["online_configure"]['enable_activity'] = player.PLAYER.online_configure.qmBZW['enable_activity']
            profile["double_seventh_logo"] = activity.ACTIVITY['double_seventh']['double_seventh_logo']
            profile["double_seventh_discount"] = activity.ACTIVITY['double_seventh']['double_seventh_discount']
            simple_channel = channel_merge(player_extra.channel)
            if simple_channel in settings.PLAYER['enable_super_package']:
                profile["online_configure"]['enable_super_package'] = True
            else:
                profile["online_configure"]['enable_super_package'] = False
            if activity.ACTIVITY['double_seventh']['double_seventh_logo']:
                first_person=player_service.get_date_gift()
                profile["double_seventh"]={}
                profile["double_seventh"]=first_person
            if player.PLAYER['vip_chat'] :
                if datetime.datetime.now().isoweekday() in player.PLAYER['vip_chat_days']:
                    profile["online_configure"]["startTime"] = 0
                    profile["online_configure"]["endTime"] = 1439
                else:
                    profile["online_configure"]["startTime"] = player.PLAYER['start_time']
                    profile["online_configure"]["endTime"] = player.PLAYER['end_time']
            for fruit in player.PLAYER['fruit_close']:
                if simple_channel == fruit['channel'] and player_extra.app_version == fruit['version']:
                    profile["online_configure"]['fruit_enabled'] = False
                    break
                else:
                    profile["online_configure"]['fruit_enabled'] = True
            for three in player.PLAYER['three_close']:
                if simple_channel == three['channel'] and player_extra.app_version == three['version']:
                    profile["online_configure"]['hundred_enabled'] = False
                    break
                else:
                    profile["online_configure"]['hundred_enabled'] = True
            for turncard in player.PLAYER['turncard_close']:
                if simple_channel == turncard['channel'] and player_extra.app_version == turncard['version']:
                    profile["online_configure"]['turncard_enabled'] = False
                    break
                else:
                    profile["online_configure"]['turncard_enabled'] = True
            profile["online_configure"]['enable_luckbag'] = settings.LUCKBAG.enable_luckbag
            if simple_channel in settings.PLAYER.online_configure.qmBZW['not_channel_bull_download']:
                profile["online_configure"]['enable_bull_download'] = False
            else:
                profile["online_configure"]['enable_bull_download'] = player.PLAYER.online_configure.qmBZW['enable_bull_download']

            if player_extra.app_version >= "2.1.1":
                profile["online_configure"]['enable_cat2currency'] = settings.CATFOOD.enable_cat2currency
            else:
                profile["online_configure"]['enable_cat2currency'] = False
            if simple_channel in settings.INVITE.off_invite_channel:
                profile["online_configure"]['enable_invite'] = False
            else:
                profile["online_configure"]['enable_invite'] = settings.INVITE.enable_invite
            serializer = self.get_serializer(profile)
        else:
            self_extra = player_models.PlayerExtra.get_player_extra(self.request.user.id)
            if self_extra.app_version < settings.VIP.vip5_version:
                if profile['vip_title'] > Vip.CROWN:
                    profile['vip_title'] = Vip.CROWN
            serializer = serializers.BriefProfile(profile)
        if user_id != self.request.user.id:
            friend_service = FriendService(request.service_repositories,
                                            request.activity_repository)
            is_friend = friend_service.already_friend(user_id, self.request.user.id)
            serializer.data['is_friend'] = is_friend

        if pk is None or request.user.id == int(pk):
            charge_moneys = player_service.get_charge_moneys(request.user.id, 3)
            today_charged_money = charge_moneys.pop(0)
            serializer.data['last_charge_moneys'] = charge_moneys
            serializer.data['today_charged_money'] = today_charged_money
            serializer.data['vip_criterials'] = settings.PLAYER.vip_criterials
            if player_extra.vip_award_steps:
                awarded_vip_titles = ujson.loads(player_extra.vip_award_steps)
            else:
                awarded_vip_titles = []
            serializer.data['awarded_vip_titles'] = awarded_vip_titles
        return Response(serializer.data)

    @trace_view
    @request_limit(serializers.UpdateProfileRequest)
    def post(self, request, format=None):
        service = PlayerService(request.service_repositories, request.activity_repository)
        serializer = serializers.UpdateProfileRequest(data=request.DATA)
        if serializer.is_valid():
            service.update_profile(request.user.id, **serializer.object)
            return Response({})
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@go.logging.class_wrapper
class UpdatePlayerAlbum(generics.CreateAPIView):

    throttle_classes = (permissions.User5SecRateThrottle,)
    serializer_class = serializers.UpdateAlbumRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    @request_limit(serializers.UpdateAlbumRequest)
    def post(self, request, format=None):
        service = PlayerService(request.service_repositories, request.activity_repository)
        serializer = serializers.UpdateAlbumRequest(data=request.DATA)
        if serializer.is_valid():
            kwargs = serializer.data
            image_url = kwargs['image_url']
            if image_url.startswith("http://") or image_url.startswith("https://"):
                service.update_album(request.user.id, **kwargs)
            else:
                kwargs['counter_repository'] = request.counter_repository
                service.update_audited_album(request.user.id, **kwargs)
            return Response({})
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@go.logging.class_wrapper
class UpdatePlayerAvatar(generics.CreateAPIView):

    throttle_classes = (permissions.User5SecRateThrottle,)
    serializer_class = serializers.UpdateAvatarRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    @request_limit(serializers.UpdateAvatarRequest)
    def post(self, request, format=None):
        service = PlayerService(request.service_repositories, request.activity_repository)
        serializer = serializers.UpdateAvatarRequest(data=request.DATA)
        if serializer.is_valid():
            service.update_avatar(request.user.id, **serializer.data)
            return Response({})
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@go.logging.class_wrapper
class DeletePlayerAlbum(generics.CreateAPIView):

    throttle_classes = (permissions.User5SecRateThrottle,)
    serializer_class = serializers.DeleteAlbumRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    @request_limit(serializers.DeleteAlbumRequest)
    def post(self, request, format=None):
        service = PlayerService(request.service_repositories, request.activity_repository)
        serializer = serializers.DeleteAlbumRequest(data=request.DATA)
        if serializer.is_valid():
            service.delete_album(request.user.id, **serializer.data)
            return Response({})
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class Deposit(generics.CreateAPIView):

    serializer_class   = serializers.DepositRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    @request_limit(serializers.DepositRequest)
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = PlayerService(request.service_repositories, request.activity_repository)
            resp = service.deposit_currency(request.user.id, **serializer.data)
            reponse_serializer = serializers.BankDetails(dict(resp._asdict()))
            return Response(reponse_serializer.data)
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class Withdraw(generics.CreateAPIView):

    serializer_class   = serializers.WithdrawRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    @request_limit(serializers.WithdrawRequest)
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = PlayerService(request.service_repositories, request.activity_repository)
            resp = service.withdraw_currency(request.user.id, **serializer.data)
            reponse_serializer = serializers.BankDetails(dict(resp._asdict()))
            return Response(reponse_serializer.data)
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class BankDetails(generics.ListAPIView):

    serializer_class   = serializers.BankDetails
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    def get(self, request, format=None, **kwargs):
        service = PlayerService(request.service_repositories, request.activity_repository)
        resp = service.get_bank_details(request.user.id)
        serializer = self.get_serializer(resp)

        return Response(serializer.data)

@go.logging.class_wrapper
class BankPassword(generics.CreateAPIView):

    serializer_class   = serializers.BankPasswordRequset
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    @request_limit(serializers.BankPasswordRequset)
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = PlayerService(request.service_repositories, request.activity_repository)
            service.change_bank_password(request.user.id, **serializer.data)
            return Response({})
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@go.logging.class_wrapper
class ForgetBankPassword(generics.CreateAPIView):

    serializer_class   = serializers.ForgetBankPasswordRequset
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            service = PlayerService(request.service_repositories, request.activity_repository)
            service.forget_bank_password(request.user.id, **serializer.data)
            return Response({})
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@go.logging.class_wrapper
class ResetBankPassword(generics.CreateAPIView):

    serializer_class   = serializers.ResetBankPasswordRequset
    template_name = 'reset-password.html'

    @trace_view
    def get(self, request, format=None):
        return TemplateResponse(
            request, self.template_name,
            {'title': '重置银行密码', 'request': request}
        )

    @trace_view
    def post(self, request, format=None):
        token = request.QUERY_PARAMS.get('token', '')
        service = PlayerService(
            request.service_repositories, request.activity_repository
        )
        serializer = self.get_serializer(data=request.DATA)
        context = {'title': '重置银行密码', 'request': request}

        if serializer.is_valid():
            try:
                service.reset_bank_password(
                    token.strip(), serializer.data['new_password']
                )
            except PlayerError.INVALID_TOKEN:
                messages.error(request, u'网页已过期')
            else:
                messages.success(request, u'密码重设成功')
            return TemplateResponse(request, self.template_name, context)
        else:
            for error in serializer.errors.values():
                if u'两次输入的密码不相同' in error:
                    messages.error(request, u'两次输入的密码不相同')
                    break
                if u'密码设置过于简单' in error:
                    messages.error(request, u'密码设置过于简单')
                    break
            else:
                messages.error(request, u'输入错误')
            return TemplateResponse(request, self.template_name, context)

@go.logging.class_wrapper
class Report(generics.CreateAPIView):

    throttle_classes = (permissions.User5SecRateThrottle,)
    serializer_class = serializers.ReportRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    @request_limit(serializers.ReportRequest)
    def post(self, request, format=None):
        service = PlayerService(request.service_repositories, request.activity_repository)
        serializer = serializers.ReportRequest(data=request.DATA)
        if serializer.is_valid():
            service.report_player(request.user.id, **serializer.data)
            return Response({})
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@go.logging.class_wrapper
class IdentifyCode(generics.CreateAPIView):

    throttle_classes = (permissions.User5SecRateThrottle,)
    serializer_class = serializers.IdentifyCodeRequest
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    @request_limit(serializers.IdentifyCodeRequest)
    def post(self, request, format=None):
        request.session["is_identified"] = False

        service = PlayerService(request.service_repositories, request.activity_repository)
        serializer = serializers.IdentifyCodeRequest(data=request.DATA)
        if request.session["identify_type"] != IdentifyType.NUMBER:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.session["is_identified"] == True:
            resp = {}
            resp["is_identified"] = True
            return Response(resp)

        if serializer.is_valid():
            resp = {}
            code = serializer.data['code']
            code = code.upper() if code is not None else ""

            award_currency = 0
            if 'code' in request.session and code == request.session["code"]:
                request.session["is_identified"] = True
                award_currency = service.update_identify_time(request.user.id, IdentifyType.NUMBER)
                captcha_manager = CaptchaManager()
                (code, image_url) = captcha_manager.generator_image(request.user.id)
                request.session["code"] = code
            else:
                captcha_manager = CaptchaManager()
                (code, image_url) = captcha_manager.generator_image(request.user.id)
                request.session["code"] = code
                resp["identify_image_url"] = image_url

            resp["is_identified"] = request.session["is_identified"]
            resp["award_currency"] = award_currency
            return Response(resp)
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class IdentifyIdiom(generics.CreateAPIView):

    throttle_classes = (permissions.User5SecRateThrottle,)
    serializer_class = serializers.IdentifyIdiomRequest
    permission_classes = (permissions.IsPlayer,)

    @trace_view
    @request_limit(serializers.IdentifyIdiomRequest)
    def post(self, request, format=None):
        request.session["is_identified"] = False

        service = PlayerService(request.service_repositories, request.activity_repository)
        serializer = serializers.IdentifyIdiomRequest(data=request.DATA)
        if request.session["identify_type"] != IdentifyType.IDIOM:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.session["is_identified"] == True:
            resp = {}
            resp["is_identified"] = True
            return Response(resp)

        if serializer.is_valid():
            resp = {}
            code = serializer.data['code']

            award_currency = 0
            if 'code' in request.session and code == request.session["code"]:
                request.session["is_identified"] = True
                idiom_manager = IdiomManager()
                code, idiom = idiom_manager.random_idiom()
                request.session["code"] = idiom
                award_currency = service.update_identify_time(request.user.id, IdentifyType.IDIOM)
            else:
                idiom_manager = IdiomManager()
                code, idiom = idiom_manager.random_idiom()
                request.session["code"] = idiom
                resp["idiom_code"] = code

            resp["is_identified"] = request.session["is_identified"]
            resp["award_currency"] = award_currency
            return Response(resp)
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@go.logging.class_wrapper
class DrawVipBag(generics.CreateAPIView):

    throttle_classes = (permissions.User5SecRateThrottle,)
    serializer_class = serializers.DrawVipBagRequest
    permission_classes = (permissions.IsIdentifiedPlayer,)

    @trace_view
    def post(self, request, format=None):
        service = PlayerService(request.service_repositories, request.activity_repository)
        serializer = self.get_serializer(data=request.DATA)
        if serializer.is_valid():
            resp = service.draw_vip_bag_award(request.user.id, **serializer.data)
            serializer = serializers.DrawVipBagResponse(resp)
            response = serializer.data
            response["vip_award_steps"] = resp["vip_award_steps"]
            return Response(response)
        else:
            from rest_framework import status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@go.logging.class_wrapper
class BeforeStart(generics.CreateAPIView):
    serializer_class = serializers.BeforeRequest
    @trace_view
    def get(self, request, format=None):
        rep = settings.PLAYER.before_start
        return Response({'show':rep})
