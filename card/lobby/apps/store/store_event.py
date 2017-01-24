from django.conf import settings

from card.core.property.three import Property
from card.core.error.common import CoreError
from card.core.charge import ITEMS

from card.lobby.apps.timeline.service import TimeLineService

class StoreEvent(object):
    
    def __init__(self, service_repositories, activity_repository):
        self.service_repositories = service_repositories
        self.activity_repository = activity_repository

    def send_charge_event(self, user_id, item_id): 
        if item_id in ITEMS.property_bags:
            item = ITEMS.property_bags[item_id]
        elif item_id in ITEMS.coins:
            item = ITEMS.coins[item_id]
        elif item_id in ITEMS.quick_coins:
            item = ITEMS.quick_coins[item_id]
        elif item_id in ITEMS.monthly_coins:
            item = ITEMS.monthly_coins[item_id]
        elif item_id in ITEMS.same_items:
            return self.send_charge_event(user_id, ITEMS.same_items[item_id].item_id)
        else:
            return
        if item_id not in ITEMS.monthly_coins:
            charge_message = settings.TIME_LINE.personal_messages.store_charge
            charge_message = charge_message.format(item.name)
        else:
            charge_message = settings.TIME_LINE.personal_messages.monthly_charge
            charge_message = charge_message.format(item.coin)
        timeline_service = TimeLineService(self.service_repositories, self.activity_repository)
        timeline_service.send_personal_message(user_id, charge_message)