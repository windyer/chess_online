from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from card.core.error.turner_error import TurnerError
import go.containers


class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        resp = self.client.post(settings.URL_PREFIX('/guest/login/'),
                                settings.GUEST_LOGIN_INFO,
                                follow=True)
        self.player_id = resp.data['id']

    def tearDown(self):
        go.containers.get_client().flushdb()

    def test_begin(self):
        resp = self.client.post(settings.URL_PREFIX('/turner/begin/'))
        self.assertIsNotNone(resp.data['suit'])
        self.assertIsNotNone(resp.data['rank'])

    def test_gaming_ok(self):
        resp = self.client.post(settings.URL_PREFIX('/turner/begin/'))
        self.assertIsNotNone(resp.data['suit'])
        self.assertIsNotNone(resp.data['rank'])

        resp = self.client.post(settings.URL_PREFIX('/turner/gaming/'),
                                {'choice': 'LARGE'})
        self.assertIsNotNone(resp.data['suit'])
        self.assertIsNotNone(resp.data['rank'])
        self.assertTrue(resp.data['status'] in ['LOSE', 'UPDATE', 'WIN'])

    def test_gaming_error(self):
        resp = self.client.post(settings.URL_PREFIX('/turner/begin/'))
        self.assertIsNotNone(resp.data['suit'])
        self.assertIsNotNone(resp.data['rank'])

        resp = self.client.post(settings.URL_PREFIX('/turner/gaming/'))
        error = TurnerError.INVALID_PARAMETER(
                    user_id=self.player_id, desc='choice is missing'
        )
        self.assertEquals(resp.data['error_code'], error.CODE)
        self.assertEquals(resp.data['error_message'], error.message)

    def test_gaming_not_start(self):
        resp = self.client.post(settings.URL_PREFIX('/turner/gaming/'),
                                {'choice': 'LARGE'})
        error = TurnerError.NOT_IN_GAME(user_id=self.player_id)
        self.assertEquals(resp.data['error_code'], error.CODE)
        self.assertEquals(resp.data['error_message'], error.message)

    def test_end_ok(self):
        resp = self.client.post(settings.URL_PREFIX('/turner/begin/'))
        self.assertIsNotNone(resp.data['suit'])
        self.assertIsNotNone(resp.data['rank'])

        resp = self.client.post(settings.URL_PREFIX('/turner/end/'))
        self.assertEquals(resp.data['win_or_lose'], True)
        self.assertEquals(resp.data['currency'], 0)
        self.assertEquals(resp.data['round'], 0)
        self.assertEquals(resp.data['cost'], 10000)

    def test_end_not_start(self):
        resp = self.client.post(settings.URL_PREFIX('/turner/end/'))
        error = TurnerError.NOT_IN_GAME(user_id=self.player_id)
        self.assertEquals(resp.data['error_code'], error.CODE)
        self.assertEquals(resp.data['error_message'], error.message)
