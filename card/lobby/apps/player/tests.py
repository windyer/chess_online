from django.test import TestCase
from django.test.client import Client
from django.conf import settings

import go.containers
from card.core.enum import Platform
import models
from .service import PlayerService


class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        go.containers.get_client().flushdb()

    def test_login(self):
        resp = self.client.post(
            settings.URL_PREFIX('/guest/login/'), settings.GUEST_LOGIN_INFO
        )
        self.assertEquals(resp.status_code, 302)

    def test_profile(self):
        resp = self.client.post(
            settings.URL_PREFIX('/guest/login/'), settings.GUEST_LOGIN_INFO,
            follow=True
        )

        self.assertEquals(resp.status_code, 200)
        player_id = resp.data['id']
        profile = settings.CREATE_PLAYER_INFO(player_id)[0]
        profile['property_items'] = settings.NEW_PLAYER_PROPERTIES()
        for attr in resp.data:
            self.assertEquals(resp.data[attr], profile[attr],
                              '%s: %s != %s' % (attr, resp.data[attr], profile[attr]))


class ModelTest(TestCase):

    def setUp(self):
        pass

    def test_player_model(self):
        p = models.Player()
        self.assertIsNone(p.save())
        self.assertIsNotNone(p.id)

    def test_profile_model(self):
        p = models.Player()
        p.save()
        profile = models.PlayerProfile()
        profile.player = p
        profile.player_type = Platform.GUEST
        self.assertIsNone(profile.save())
        self.assertEquals(profile.player, p)
        self.assertIsNotNone(profile.created_time)
        self.assertIsNone(profile.last_login_time)


class ServiceTest(TestCase):

    def setUp(self):
        resp = self.client.post(
            settings.URL_PREFIX('/guest/login/'), settings.GUEST_LOGIN_INFO,
            follow=True
        )

        self.assertEquals(resp.status_code, 200)
        self.player_id = resp.data['id']
        from card.lobby.service.mock.service_repository import ServiceRepository
        self.service = PlayerService(ServiceRepository())

    def test_update_currency(self):
        resp = self.service.update_currency(self.player_id, 10000)
        self.assertEquals(resp.currency, 10000)

    def test_login(self):
        resp = self.service.login(self.player_id)
        self.assertIsNotNone(resp)
