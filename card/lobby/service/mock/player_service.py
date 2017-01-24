__all__ = ['PlayerService']

from collections import namedtuple
from go.util import DotDict
from datetime import datetime

class PlayerService(object):

    def get_profile(self, user_id):
        user_id = int(user_id)
        profile = {'user_id': user_id,
                   'nick_name': 'nick_name_%d' % user_id,
                   'gender': 'unknown',
                   'avatar_url': 'avatar_%d' % user_id,
                   'currency': user_id,
                   'total_rounds': user_id,
                   'total_win_rounds': user_id,
                   'total_lose_rounds': user_id,
                   'round_max_win': user_id,
                   'total_max_currency': user_id,
                   'max_hand_card': '',
                   'room_id': user_id,
                   'last_login_time':datetime.utcnow(),
                   'continuous_login_days':user_id}
        return namedtuple('profile', profile)(**profile)

    def get_profiles(self, *users_id):
        profiles = [self.get_profile(user_id) for user_id in users_id]
        return profiles

    def update_profile(self, user_id, **kwargs):
        pass

    def update_currency(self, user_id, delta_currency):
        return DotDict({'currency': delta_currency})
        
    def login(self, user_id):
        return DotDict()
