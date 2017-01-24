__all__ = ['PropertyService']

from card.lobby.apps.property import models

class PropertyService(object):

    def get_items(self, user_id):

    	return models.PlayerProperty.objects.all()

    def increment_items(self, user_id, *items):
        return {}

    def decrement_items(self, user_id, *items):
        return {}
