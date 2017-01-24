from card.lobby.service.view_service import ViewService
from card.lobby.apps.player.service import PlayerService
from card.core.property.three import Property
from card.lobby.apps.player.models import Player
from django.conf import settings
import time
from go.containers import redis
from card.core.error.lobby import LuckbagError
import random


class LuckbagService(ViewService):
    def __init__(self, service_repositories, activity_repository):
        super(LuckbagService, self).__init__(service_repositories, activity_repository)


    def luckbag(self,user_id,click_time):
        re = redis.Redis(**settings.PERSIST_REDIS)
        player = Player.get_player(user_id)
        nick_name = player.nick_name.encode('utf8')
        luck_player_name = re.lrange('luck_player_name', 0, 100)
        luck_player_currency = re.lrange('luck_player_currency', 0, 100)
        luck_players = []
        for (i, j) in zip(luck_player_name, luck_player_currency):
            luck_players.append({i: j})
        if nick_name in luck_player_name:
            return {'currency': 0, 'luck_players': [], 'result_code': 431001}
        if len(luck_player_name) >= 100 :
            return {'currency':0,'luck_players':luck_players,'result_code':0}
        player_service=PlayerService(self.service_repositories,self.activity_repository)
        response = player_service.luck_bag(user_id,click_time)
        currency = response.random_currency
        rate = random.random()
        if rate > settings.LUCKBAG.luck_bag_rate:
            currency = 0
            return {'currency': 0, 'luck_players': luck_players, 'result_code': 0}
        if currency == 0 :
            return {'currency': 0, 'luck_players': luck_players, 'result_code': 0}
        re.lpush('luck_player_name',nick_name)
        re.lpush('luck_player_currency',currency)
        re.expire('luck_player_name', settings.LUCKBAG.continue_time)
        re.expire('luck_player_currency', settings.LUCKBAG.continue_time)
        luck_players.append({nick_name:currency})
        player_service.increment_currency(user_id,currency,'luck_bag')
        return {'currency':currency,'luck_players':luck_players,'result_code': 0}