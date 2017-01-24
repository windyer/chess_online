from django.conf import settings
from card.core.error.common import CoreError

class TurnerEvent(object):
    
    def __init__(self, service_repositories, counter_repository):
        self.service_repositories = service_repositories
        self.counter_repository = counter_repository

    def send_turner_event(self, user_id, award_currency):
        max_round = settings.TURNER.max_round
        if award_currency == settings.TURNER.award_currencys[max_round]:
            player_service = self.service_repositories.db.player_service
            profile = player_service.get_profile(user_id)
            try:
                bulletin_service = self.service_repositories.chat.bulletin_service
                bulletin_service.send_turner_event(user_id=user_id, nick_name=profile.nick_name, 
                                                currency=award_currency)
            except CoreError.CHAT_CONNECTION_FAILED:
                pass

            for counter in self.counter_repository.counters:
                counter.incr(user_id, **{'turner_million_count':1})
