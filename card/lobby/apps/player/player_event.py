from card.core.charge import ITEMS

from django.conf import settings

class PlayerEvent(object):
    
    def __init__(self, service_repositories, activity_repository):
        self.service_repositories = service_repositories
        self.activity_repository = activity_repository

    def send_monthly_payment_event(self, user_id, item_id): 
        if item_id in ITEMS.monthly_coins:
            item = ITEMS.monthly_coins[item_id]
        else:
            return

        charge_message = settings.TIME_LINE.personal_messages.monthly_charge
        charge_message = charge_message.format(item.coin)
        
        from card.lobby.apps.timeline.service import TimeLineService
        timeline_service = TimeLineService(self.service_repositories, self.activity_repository)
        timeline_service.send_personal_message(user_id, charge_message)