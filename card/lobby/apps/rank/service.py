import redis
from datetime import date
import datetime

from django.conf import settings

from go.containers import containers

from card.core.enum import Rank

from card.lobby.service.view_service import ViewService
from card.lobby.apps.player.service import PlayerService
from card.lobby.aop import cache_top_rank
import ujson

class RankService(ViewService):

    def get_user_rank(self, user_id, rank_name):
        re = redis.Redis(**settings.PERSIST_REDIS)
        sorted_set = containers.SortedSet(rank_name, db=re)
        user_rank = sorted_set.zrevrank(user_id)

        if user_rank is not None:
            user_rank = int(user_rank)+1

        return user_rank

    def get_user_ranks(self, user_id):
        ranks = {}
        ranks['currency'] = self.get_user_rank(user_id, Rank.CURRENCY)
        ranks['gift'] = self.get_user_rank(user_id, Rank.GIFT)
        today_income_most_key = Rank.TODAY_INCOME_MOST.format(date.today())
        ranks['today_income_most'] = self.get_user_rank(user_id, today_income_most_key)
        return ranks

    @cache_top_rank
    def get_top_rank(self, rank_name, max_rank=settings.RANK.max_size):
        if rank_name == Rank.TODAY_INCOME_MOST:
            rank_key = rank_name.format(date.today())
        elif rank_name == Rank.FRUIT_WEEK_INCOME_MOST:
            calendar = date.today().isocalendar()
            week_string = "{0}-{1}".format(calendar[0], calendar[1])
            rank_key = rank_name.format(week_string)
        elif rank_name == Rank.RED_ENVELOPE_MONTHLY_SEND_MOST:
            today = datetime.datetime.today()
            month_string = "{0}-{1}".format(today.year, today.month)
            rank_key = rank_name.format(month_string)
        else:
            rank_key = rank_name

        players = []
        re = redis.Redis(**settings.PERSIST_REDIS)
        if rank_name == Rank.JACKPOT_AWARD:
            award_list = containers.List(rank_key, db=re)
            msgs = award_list.lrange(0, max_rank)
            player_service = PlayerService(self.service_repositories, self.activity_repository)
            for msg in msgs:
                user = ujson.loads(msg)
                profile = player_service.get_profile(user['user_id'])
                profile = profile._asdict()
                profile['jackpot_award'] = user['award_currency']
                profile['jackpot_stamp'] = user['time_stamp']
                players.append(profile)

            return players

        sorted_set = containers.SortedSet(rank_key, db=re)        
        user_ids = map(int, sorted_set.zrevrange(0, max_rank))

        player_service = PlayerService(self.service_repositories, self.activity_repository)
        profiles = player_service.get_profiles(*user_ids)

        for profile in profiles:
            profile = profile._asdict()
            if rank_name.startswith(Rank.TODAY_INCOME_MOST):
                profile['today_income_most'] = int(sorted_set.zscore(profile['user_id']))
            elif rank_name.startswith(Rank.FRUIT_WEEK_INCOME_MOST):
                profile['week_fruit_income_most'] = int(sorted_set.zscore(profile['user_id']))
            elif rank_name.startswith(Rank.RED_ENVELOPE_MONTHLY_SEND_MOST):
                profile['monthly_red_envelope_send_most'] = int(sorted_set.zscore(profile['user_id']))
            elif rank_name.startswith(Rank.THREE_WIN_CHAMPIONSHIP):
                profile['three_win_currency'] = int(sorted_set.zscore(profile['user_id']))
            elif rank_name.startswith(Rank.FRUIT_WIN_CHAMPIONSHIP):
                profile['fruit_win_currency'] = int(sorted_set.zscore(profile['user_id']))
            elif rank_name.startswith(Rank.JACKPOT_CURRENCY):
                profile['jackpot_currency'] = int(sorted_set.zscore(profile['user_id']))            
            players.append(profile)

        return players

    def yesterday_win_rank(self, user_id):
        yesterday = date.today() - datetime.timedelta(days=1)
        income_most_key = Rank.TODAY_INCOME_MOST.format(yesterday)        
        return self.get_user_rank(user_id, income_most_key)