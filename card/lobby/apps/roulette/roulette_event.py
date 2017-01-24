from card.core.property.three import Property
from card.core.error.common import CoreError

class RouletteEvent(object):
    
    def __init__(self, service_repositories):
        self.service_repositories = service_repositories

    def send_roulette_gift_event(self, user_id, roulette_item_id):   
        pass    