__all__ = ['ServiceRepository']

from go.protobuf import NetworkError

from game_service import GameService
from room_service import RoomService
from social_service import SocialService
from player_service import PlayerService
from property_service import PropertyService

class ServiceRepository(object):

    def __init__(self):
        try:
            self.player_service = PlayerService() 
            self.game_service = GameService()
            self.property_service = PropertyService()
            self.room_service = RoomService()
            self.social_service = SocialService()
        except NetworkError.CONNECTION_FAILED:
            raise CoreError.DB_CONNECTION_FAILED()
            
    def close(self):
        self.player_service = None
        self.game_service = None
        self.property_service = None
        self.room_service = None
        self.social_service = None
