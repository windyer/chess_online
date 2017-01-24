from django.test import TestCase
from django.test.client import Client
from django.conf import settings

import go.containers

from card.core.error.lobby.game_error import GameError

class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        response = self.client.post(
            settings.URL_PREFIX('/guest/login/'), settings.GUEST_LOGIN_INFO,
            follow=True
        )

        self.assertEquals(response.status_code, 200)
        self.player_id = response.data['id']

    def tearDown(self):
        go.containers.get_client().flushdb()

    def test_quick_game(self):
        resp = self.client.post(settings.URL_PREFIX('/game/quick/'))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data,
                          {'game': {'game_id': 1,
                                    'host': 'localhost',
                                    'port': 10087},
                           'token': self.player_id})

    def test_select_game(self):
        resp = self.client.post(settings.URL_PREFIX('/game/select/'),
                                data={'mode': 1, 'level': 1})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data,
                          {'game': {'game_id': 1,
                                    'host': 'localhost',
                                    'port': 10087},
                           'token': self.player_id})

    def test_select_game_missing_mode(self):
        resp = self.client.post(settings.URL_PREFIX('/game/select/'),
                                data={'level': 1})
        error = GameError.INVALID_MODE(
            user_id=self.player_id, mode=None
        )
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error_code'], error.CODE)
        self.assertEquals(resp.data['error_message'], error.message)

    def test_select_game_missing_level(self):
        resp = self.client.post(settings.URL_PREFIX('/game/select/'),
                                data={'mode': 1})
        error = GameError.INVALID_LEVEL(
            user_id=self.player_id, level=None
        )
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error_code'], error.CODE)
        self.assertEquals(resp.data['error_message'], error.message)

    def test_follow_game(self):
        resp = self.client.post(settings.URL_PREFIX('/game/follow/'),
                                data={'friend_id': self.player_id})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data,
                          {'game': {'game_id': 1,
                                    'host': 'localhost',
                                    'port': 10087},
                           'token': self.player_id})
