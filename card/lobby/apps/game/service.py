from datetime import datetime, timedelta
from django.conf import settings

from card.core.util.timestamp import get_timestamp_for
from card.lobby.extensions.logging import mongo_logger
from card.lobby.service.view_service import ViewService
from card.lobby.apps.player.redis import PlayerExtra
import card.lobby.apps.player.models as player_models

class GameService(ViewService):

    def _unmark_silent_users(self, user_id):
        player_extra = player_models.PlayerExtra.get_player_extra(user_id)
        if not player_extra.created_today:
            return
        now = datetime.now()
        start = now - timedelta(**settings.HOLYTREE.silent_user_interval)
        spec = {
            'user_id': user_id,
            'timestamp': {
                '$gte': get_timestamp_for(start, unit='ms'),
                '$lte': get_timestamp_for(now, unit='ms')
            },
            'silent_user': True,
        }
        player_register = mongo_logger.mongodb.player_register
        player_register.find_and_modify(spec, {'$set': {'silent_user': False}})

    def quick_game(self, user_id):
        try:
            resp = self.service_repositories.db.game_service.quick_game(user_id=user_id)
        except Exception as ex:
            print ex
            raise ex
        self._unmark_silent_users(user_id)

        return resp

    def select_game(self, user_id, mode, level):
        try:
            resp = self.service_repositories.db.game_service.select_game(
                user_id, mode=mode, level=level)
        except Exception as ex:
            print ex
            raise ex
        self._unmark_silent_users(user_id)

        return resp

    def follow_game(self, user_id, target_user_id):
        try:
            resp = self.service_repositories.db.game_service.follow_game(
                    user_id=user_id, target_user_id=target_user_id)
        except Exception as ex:
            print ex
            raise ex
        self._unmark_silent_users(user_id)

        return resp

    def get_concurrency(self):
        if not settings.GAME.display_concurrency:
            return 0
        monitor_service = self.service_repositories.db.monitor_service
        online_status = monitor_service.get_concurrency()
        return int(online_status.concurrent_users * settings.GAME.concurrency_times)
