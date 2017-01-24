from collections import defaultdict

from go import containers
from go.containers import redis
from go.containers.containers import Hash
from go import model

from django.utils import timezone
from django.conf import settings


class SessionStatus(model.Model):
    status = model.CharField()
    current_round = model.IntegerField(default=0)
    exclude_ranks = model.ListField(int)
    current_rank = model.IntegerField()
    cost = model.IntegerField()
    expire_time = model.DateTimeField()
    good_luck = model.BooleanField(default=False)

    class Meta:
        db = containers.get_client()
        auto_increment = False

    def update_expire_time(self):
        self.expire_time = timezone.now() + \
                    timezone.timedelta(seconds=settings.TURNER.session_expire)
                    
    @staticmethod
    def create(user_id, good_luck=False):
        cost = settings.TURNER.cost
        expire_time = timezone.now() + \
                    timezone.timedelta(seconds=settings.TURNER.session_expire)

        session_status = SessionStatus.objects.create(status=settings.TURNER.status.pending, 
                current_round=0, exclude_ranks=[], cost=cost,  expire_time=expire_time,
                good_luck=good_luck)
        session_status.set_id(user_id)

        return session_status

    @staticmethod
    def get_status(user_id):
        return SessionStatus.objects.get_by_id(user_id)

    @staticmethod
    def is_exists(user_id):
        if SessionStatus.exists(user_id):
            session_status = SessionStatus.objects.get_by_id(user_id)
            if (session_status is not None and session_status.expire_time > timezone.now()):
                return True
            else:
                session_status.delete()
        return False


class TurnerStatistics(object):

    round_statistics = Hash('TurnerStatistics:Round:Counter', redis.Redis(**settings.PERSIST_REDIS))
    total_round_key = '100'

    def incr_win_rounds(self, round):
        assert round >=0 and round <=4
        if round:
            self.round_statistics.hincrby(round, 1)

    def incr_total_rounds(self):
        self.round_statistics.hincrby(self.total_round_key, 1)
     
    @property
    def profit_margin(self):
        round_stat = defaultdict(int, self.round_statistics.hgetall())
        player_pay = (0 if self.total_round_key not in round_stat else
                    settings.TURNER.cost * int(round_stat[self.total_round_key]))

        system_lose = 0
        for round in xrange(1, settings.TURNER.max_round + 1):
            if str(round) in round_stat:
                system_lose += int(round_stat[str(round)]) * settings.TURNER.award_currencys[round]

        return (settings.TURNER.profit_margin.high_criteria if not system_lose else
                player_pay / float(system_lose))
