from card.core.error.common import CoreError
from django.conf import settings

class DailyEvent(object):
    
    def __init__(self, service_repositories):
        self.service_repositories = service_repositories

    def send_fortune_cat_event(self, user_id, currency):       
        if currency >= settings.DAILY.cat_award_criteria:
            player_service = self.service_repositories.db.player_service
            profile = player_service.get_profile(user_id)

            try:
                bulletin_service = self.service_repositories.chat.bulletin_service
                bulletin_service.send_fortune_cat_event(user_id=user_id, nick_name=profile.nick_name, 
                                            currency=currency)
            except CoreError.CHAT_CONNECTION_FAILED:
                pass