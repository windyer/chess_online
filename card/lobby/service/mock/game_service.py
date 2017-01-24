__all__ = ['GameService']

class GameService(object):

    def quick_game(self, user_id):
        return {'game': {'game_id': 1, 'host': 'localhost', 'port': 10087},
                'token': user_id}

    def select_game(self, user_id, mode, level):
        return {'game': {'game_id': 1, 'host': 'localhost', 'port': 10087},
                'token': user_id}

    def follow_game(self, user_id, target_user_id):
        target_user_id = int(target_user_id)
        return {'game': {'game_id': 1, 'host': 'localhost', 'port': 10087},
                'token': target_user_id}
