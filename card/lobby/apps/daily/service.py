import time

from django.conf import settings

import go.logging
from go.containers.containers import Set
from go.containers import redis
from go.util import DotDict

from card.lobby.aop.logging import trace_service
from card.core.util.timestamp import get_day_begin
from card.core.error.lobby.daily_error import DailyError
from card.core.property.three import Property
from card.lobby.apps.daily.daily_event import DailyEvent

from card.lobby.service.view_service import ViewService
from card.lobby.apps.player.service import PlayerService
from card.lobby.apps.rank.service import RankService
import card.lobby.apps.player.models as player_models
from card.lobby.apps.timeline.service import TimeLineService
from card.lobby.apps.daily.redis import OnlineAwardStatus

@go.logging.class_wrapper
class DailyService(ViewService):

    def _device_awarded(self, device_id):
        re = redis.Redis(**settings.PERSIST_REDIS)
        awarded_devices = Set(settings.DAILY.login_awarded_device_set, re)
        if device_id in awarded_devices:
            return True
        else:
            False

    def _yesterday_rank(self, user_id):
        rank_service = RankService(self.service_repositories, self.activity_repository)
        return rank_service.yesterday_win_rank(user_id)

    def _login_awards(self, continuous_login_days, device_id, user_id):
        if continuous_login_days == 0 or self._device_awarded(device_id):
            login_award = 0
        elif (continuous_login_days > settings.DAILY.login_award.max_days):
            login_award = settings.DAILY.login_award.award_base + \
            settings.DAILY.login_award.max_days * settings.DAILY.login_award.award_increment
        else:
            login_award = settings.DAILY.login_award.award_base + \
            continuous_login_days * settings.DAILY.login_award.award_increment


        special_award = self._special_award(user_id)
        login_award += special_award
        
        return [DotDict({'item_id':Property.COIN.item_id, 'count':login_award}),]

    def _rank_awards(self, user_id):
        yesterday_rank = self._yesterday_rank(user_id)
        if yesterday_rank in settings.DAILY.rank_awards:
            return settings.DAILY.rank_awards[yesterday_rank]

    def _vip_awards(self, vip_title):
        return settings.VIP.daily_awards[vip_title]

    def _monthly_payment_award(self, user_id):
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        if not player_extra.is_monthly_player:
            return None
        if settings.DAILY.monthly_payment_award <= 0:
            return None

        return [DotDict({'item_id':Property.COIN.item_id, 'count':settings.DAILY.monthly_payment_award}),]

    def _fortune_cat_award(self, user_id, cat_weight):
        if cat_weight <= 0:
            return None
        return [DotDict({'item_id':Property.COIN.item_id, 'count':cat_weight * 1000}),]

    def _increment_awards(self, user_id, award_items, reason):
        if award_items is None:
            return
        player_service = PlayerService(self.service_repositories, self.activity_repository)
        for item in award_items:
            if item.count <= 0:
                continue
            if item.item_id == Property.COIN:
                player_service.increment_currency(user_id, item.count, reason)
            else:
                player_service.increment_item(user_id, item.item_id, item.count)


    def _send_personal_message(self, user_id, continuous_login_days, vip_title,
                            vip_awards, login_awards, rank_awards, monthly_payment_award, fortune_cat_award):
        timeline_service = TimeLineService(self.service_repositories, self.activity_repository)
        if login_awards is not None:
            for item in login_awards:
                item_name = settings.STORE.item_names[item.item_id]
                message = settings.DAILY.messages.continous_login.format(continuous_login_days, item.count, item_name)
                timeline_service.send_personal_message(user_id, message)
        if vip_awards is not None:
            for item in vip_awards:
                item_name = settings.STORE.item_names[item.item_id]
                title = settings.PLAYER.vip_titles[vip_title]
                message = settings.DAILY.messages.vip_award.format(title, item.count, item_name)
                timeline_service.send_personal_message(user_id, message)
        if rank_awards is not None:
            yesterday_rank = self._yesterday_rank(user_id)
            for item in rank_awards:
                item_name = settings.STORE.item_names[item.item_id]
                message = settings.DAILY.messages.rank_ward.format(yesterday_rank, item.count, item_name)
                timeline_service.send_personal_message(user_id, message)
        if monthly_payment_award is not None:
            for item in monthly_payment_award:
                item_name = settings.STORE.item_names[item.item_id]
                message = settings.DAILY.messages.monthly_payment_award.format(item.count, item_name)
                timeline_service.send_personal_message(user_id, message)
        if fortune_cat_award is not None:
            message = settings.DAILY.messages.fortune_cat_award
            message = message.format(fortune_cat_award[0].count)
            timeline_service.send_personal_message(user_id, message)
            daily_event = DailyEvent(self.service_repositories)
            daily_event.send_fortune_cat_event(user_id, fortune_cat_award[0].count)

    def get_daily_status(self, user_id, continuous_login_days, vip_title, device_id):
        re = redis.Redis(**settings.PERSIST_REDIS)
        award_players = Set(settings.DAILY.awarded_player_set, re)
        max_login_award = settings.DAILY.login_award.award_base + \
            settings.DAILY.login_award.max_days * settings.DAILY.login_award.award_increment

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)

        resp = {}
        resp['daily_awarded'] = True if user_id in award_players else False
        resp['max_login_award'] = max_login_award
        resp['login_awards'] = self._login_awards(continuous_login_days, device_id, user_id)
        resp['rank_awards'] = self._rank_awards(user_id)
        resp['vip_awards'] = self._vip_awards(vip_title)
        resp['monthly_payment_award'] = self._monthly_payment_award(user_id)
        resp['fortune_cat_awards'] = self._fortune_cat_award(user_id, profile.cat_weight)
        return resp

    def _special_award(self, user_id):
        draw_activities = self.activity_repository.draw_activities
        for activity_id in draw_activities:
            activity = draw_activities[activity_id]
            if hasattr(activity, 'special_award'):
                return activity.special_award(user_id)
        return 0

    @trace_service
    def get_daily_award(self, user_id):
        re = redis.Redis(**settings.PERSIST_REDIS)
        award_players = Set(settings.DAILY.awarded_player_set, re)
        if user_id in award_players:
            raise DailyError.HAS_AWARDED(user_id=user_id)

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)

        login_awards = self._login_awards(player_extra.continuous_login_days, player_extra.login_device_id, user_id)
        vip_awards = self._vip_awards(profile.vip_title)
        rank_awards = self._rank_awards(user_id)        
        monthly_payment_award = self._monthly_payment_award(user_id)
        fortune_cat_awards = self._fortune_cat_award(user_id, profile.cat_weight)

        self._increment_awards(user_id, login_awards, "daily_award")
        self._increment_awards(user_id, vip_awards, 'vip_daily_award')
        self._increment_awards(user_id, rank_awards, 'rank_challenge_awards')
        self._increment_awards(user_id, monthly_payment_award, "monthly_payment_daily_award")
        self._increment_awards(user_id, fortune_cat_awards, "fortune_cat_award")

        now_timestamp = time.time()
        today_end = get_day_begin(timestamp=now_timestamp, N=1)
        ttl = int(today_end - now_timestamp)
        award_players.add(user_id)
        award_players.set_expire(ttl)
        login_awarded_devices = Set(settings.DAILY.login_awarded_device_set, re)
        login_awarded_devices.add(player_extra.login_device_id)
        login_awarded_devices.set_expire(ttl)

        self._send_personal_message(user_id, player_extra.continuous_login_days, 
                                profile.vip_title, vip_awards, login_awards, rank_awards,
                                monthly_payment_award, fortune_cat_awards)

        resp = {}
        profile = player_service.get_profile(user_id)
        resp['currency'] = profile.currency
        resp['login_awards'] = login_awards
        resp['rank_awards'] = rank_awards
        resp['vip_awards'] = vip_awards
        resp['fortune_cat_awards'] = fortune_cat_awards
        resp['monthly_payment_award'] = monthly_payment_award

        return resp

    @trace_service
    def get_online_award(self, user_id):
        online_award = OnlineAwardStatus()
        award_step = online_award.next_award_step(user_id)
        max_award_step = max(settings.DAILY.online_awards.keys())
        if award_step > max_award_step:
            raise DailyError.HAS_AWARDED(user_id=user_id)

        assert award_step <= max_award_step
        awerd_interval = award_step * 60

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profile = player_service.get_profile(user_id)
        gamed_time = profile.gamed_time
        if gamed_time < awerd_interval:
            raise DailyError.NOT_REACH_LIMITATION(user_id=user_id, award_step=award_step)

        assert award_step in settings.DAILY.online_awards
        award_currency = settings.DAILY.online_awards[award_step]
        if award_currency > 0:
            player_service.increment_currency(user_id, award_currency, 'online_award')
        player_service.reset_gamed_time(user_id)
        online_award.draw_award(user_id, award_step)

        next_award_step = self.get_next_online_award_step(user_id)
        resp = {}
        resp["award_currency"] = award_currency
        resp["next_award_step"] = next_award_step
        return resp

    def get_next_online_award_step(self, user_id):
        online_award = OnlineAwardStatus()
        next_award_step = online_award.next_award_step(user_id)
        max_award_step = max(settings.DAILY.online_awards.keys())
        if next_award_step > max_award_step:
            next_award_step = 0

        return next_award_step