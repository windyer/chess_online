from django.test import TestCase
from django.test.client import Client
from django.conf import settings
import go.containers

from card.core.error.lobby.store_error import StoreError
from card.lobby.apps.property.registry import item_repository


def sell_item(self, user_id, item_id, count):
    if not item_repository.has_item(item_id):
        raise StoreError.NO_SUCH_ITEM(user_id=user_id, item_id=item_id)
    return {'player_id': user_id, 'item_id': item_id,
            'count': count, 'earn': item_id * count}
from service import StoreService
StoreService.sell_item = sell_item


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

    def test_purchase_ok(self):
        resp = self.client.post(
                settings.URL_PREFIX('/store/purchase/'),
                data={'item_id': 101, 'count': 1},
        )
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data, {'player_id': self.player_id,
                                      'item_id': 101,
                                      'count': 1,
                                      'cost': 5000})

    def test_purchase_invalid_item(self):
        resp = self.client.post(
                settings.URL_PREFIX('/store/purchase/'),
                data={'item_id': -1, 'count': 1},
        )
        self.assertEquals(resp.status_code, 200)
        error = StoreError.NO_SUCH_ITEM_ON_SALE(
            user_id=self.player_id, item_id=-1
        )
        self.assertEquals(resp.data, {'error_code': error.CODE,
                                      'error_message': error.message})

    def test_sell_ok(self):
        resp = self.client.post(
                settings.URL_PREFIX('/store/sell/'),
                data={'item_id': 101, 'count': 1},
        )
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data, {'player_id': self.player_id,
                                      'item_id': 101,
                                      'count': 1,
                                      'earn': 101*1})

    def test_sell_invalid_item(self):
        resp = self.client.post(
                settings.URL_PREFIX('/store/sell/'),
                data={'item_id': -1, 'count': 1},
        )
        self.assertEquals(resp.status_code, 200)
        error = StoreError.NO_SUCH_ITEM(user_id=self.player_id, item_id=-1)
        self.assertEquals(resp.data, {'error_code': error.CODE,
                                      'error_message': error.message})
