from django.conf import settings

from card.lobby.apps.turner.models import TurnerLog

class TurnerLogger(object):

    def record_round_result(self, user_id, award_currency, round, status):
        turner_log = TurnerLog()
        turner_log.user_id = user_id
        turner_log.round = round
        turner_log.win_or_lose = status
        turner_log.award_currency = award_currency if status == settings.TURNER.status.win else 0
        turner_log.cost = settings.TURNER.cost
        turner_log.save()
