from django.conf import settings
from card.core.error.common import CoreError

from card.lobby.apps.timeline.service import TimeLineService

class FreebieEvent(object):
    
    def __init__(self, service_repositories, activity_repository):
        self.service_repositories = service_repositories
        self.activity_repository = activity_repository

    def send_score_wall_event(self, user_id, award_currency):
        score_wall_message = settings.TIME_LINE.personal_messages.score_wall_award
        score_wall_message = score_wall_message.format(award_currency)
        timeline_service = TimeLineService(self.service_repositories, self.activity_repository)
        timeline_service.send_personal_message(user_id, score_wall_message)
        
        player_service = self.service_repositories.db.player_service
        profile = player_service.get_profile(user_id)
        try:
            bulletin_service = self.service_repositories.chat.bulletin_service
            bulletin_service.send_score_wall_event(user_id=user_id, nick_name=profile.nick_name, 
                                            currency=award_currency)
        except CoreError.CHAT_CONNECTION_FAILED:
            pass