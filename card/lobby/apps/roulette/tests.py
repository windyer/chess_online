from django.test import TestCase
from django.test.client import Client
from django.conf import settings


class ViewTest(TestCase):

    def test_roulette(self):
        client = Client()
        client.post(settings.URL_PREFIX('/guest/login/'),
                    settings.GUEST_LOGIN_INFO)

        resp = client.post(settings.URL_PREFIX('/roulette/'))
        self.assertIsNotNone(resp.data['item_id'])
        self.assertIsNotNone(resp.data['name'])
        self.assertIsNotNone(resp.data['count'])
