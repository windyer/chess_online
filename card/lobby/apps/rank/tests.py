from django.test import TestCase
from django.test.client import Client
from django.conf import settings
import go.containers


class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        response = self.client.post(
            settings.URL_PREFIX('/guest/login/'), settings.GUEST_LOGIN_INFO,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.player_id = response.data['id']

    def tearDown(self):
        go.containers.get_client().flushdb()

    def test_player_rank(self):
        resp = self.client.get(settings.URL_PREFIX('/rank/rank/'))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data, {'currency': 1,
                                      'gift': 1, 'today_income_most': 1})

    def test_currency_rank(self):
        resp = self.client.get(settings.URL_PREFIX('/rank/currency/'))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['count'], settings.MAX_RANK)
        self.assertIsNone(resp.data['previous'])
        self.assertIsNotNone(resp.data['next'])
        self.assertEquals(len(resp.data['results']), 10)

    def test_gift_rank(self):
        resp = self.client.get(settings.URL_PREFIX('/rank/gift/'))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['count'], settings.MAX_RANK)
        self.assertIsNone(resp.data['previous'])
        self.assertIsNotNone(resp.data['next'])
        self.assertEquals(len(resp.data['results']), 10)

    def test_today_income_most(self):
        resp = self.client.get(settings.URL_PREFIX('/rank/today-income-most/'))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['count'], settings.MAX_RANK)
        self.assertIsNone(resp.data['previous'])
        self.assertIsNotNone(resp.data['next'])
        self.assertEquals(len(resp.data['results']), 10)
