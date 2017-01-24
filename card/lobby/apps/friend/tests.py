from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from django.utils import timezone

import go.containers

from card.lobby.apps.player.models import Player, PlayerProfile
from card.lobby.apps.friend import models
from card.lobby.apps.friend.redis import Friendship as RFriendship
from card.core.error.lobby.friend_error import FriendError


class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        resp = self.client.post(
            settings.URL_PREFIX('/guest/login/'), settings.GUEST_LOGIN_INFO,
            follow=True
        )
        self.assertEquals(resp.status_code, 200)
        self.player_id = resp.data['id']

        self.friend = Player()
        self.friend.save()

        profile = PlayerProfile()
        profile.player = self.friend
        profile.player_type = 1
        profile.save()

    def tearDown(self):
        go.containers.get_client().flushdb()

    def _create_friendship(self, redis=False):
        if redis:
            friendship = RFriendship()
            friendship.player_id = self.player_id
            friendship.friend_id = self.friend.id
            friendship.created_time = timezone.now()
            assert friendship.is_valid(), friendship.errors
            friendship.save()
        else:
            player = Player.objects.get(pk=self.player_id)
            friendship = models.Friendship()
            friendship.player = player
            friendship.friend = self.friend
            friendship.save()

    def _create_request(self, replied=False):
        request = models.FriendshipRequestLog()
        request.user_id = self.friend.id
        request.target_user_id = self.player_id
        if replied:
            request.replied_time = timezone.now()
        request.save()

    def test_friend_list(self):
        self._create_friendship(redis=True)
        resp = self.client.get(settings.URL_PREFIX('/friend/friends/'))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['count'], 1)
        self.assertEquals(resp.data['results'][0]['friend_id'], self.friend.id)

    def test_request_friendship(self):
        resp = self.client.post(settings.URL_PREFIX('/friend/request/'),
                                data={'target_user_id': self.friend.id})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['player_id'], self.player_id)
        self.assertEquals(resp.data['target_user_id'], self.friend.id)
        self.assertEquals(resp.data['status'], settings.PENDING)

    def test_request_self(self):
        resp = self.client.post(settings.URL_PREFIX('/friend/request/'),
                                data={'target_user_id': self.player_id})
        self.assertEquals(resp.status_code, 200)
        error = FriendError.REQUESTING_SELF(user_id=self.player_id)
        self.assertEquals(resp.data['error_code'], error.CODE)
        self.assertEquals(resp.data['error_message'], error.message)

    def test_request_already_friend(self):
        self._create_friendship()
        resp = self.client.post(settings.URL_PREFIX('/friend/request/'),
                                data={'target_user_id': self.friend.id})
        self.assertEquals(resp.status_code, 200)
        error = FriendError.ALREADY_FRIEND(
            user_id=self.player_id, friend_id=self.friend.id
        )
        self.assertEquals(resp.data['error_code'], error.CODE)
        self.assertEquals(resp.data['error_message'], error.message)

    def test_request_missing_friend_id(self):
        resp = self.client.post(settings.URL_PREFIX('/friend/request/'))
        self.assertEquals(resp.status_code, 200)
        error = FriendError.INVALID_TARGET(
            user_id=self.player_id, target_user_id=None
        )
        self.assertEquals(resp.data['error_code'], error.CODE)
        self.assertEquals(resp.data['error_message'], error.message)

    def test_reply_friendship_accepted(self):
        self._create_request()
        resp = self.client.post(settings.URL_PREFIX('/friend/reply/'),
                                data={'request_sender': self.friend.id,
                                      'status': settings.ACCEPTED})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['player_id'], self.friend.id)
        self.assertEquals(resp.data['target_user_id'], self.player_id)
        self.assertEquals(resp.data['status'], settings.ACCEPTED)
        self.assertIsNotNone(resp.data['replied_time'])

    def test_reply_friendship_declined(self):
        self._create_request()
        resp = self.client.post(settings.URL_PREFIX('/friend/reply/'),
                                data={'request_sender': self.friend.id,
                                      'status': settings.DECLINED})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['player_id'], self.friend.id)
        self.assertEquals(resp.data['target_user_id'], self.player_id)
        self.assertEquals(resp.data['status'], settings.DECLINED)
        self.assertIsNotNone(resp.data['replied_time'])

    def test_reply_missing_request_sender(self):
        self._create_request()
        resp = self.client.post(settings.URL_PREFIX('/friend/reply/'),
                                data={'status': settings.ACCEPTED})
        self.assertEquals(resp.status_code, 200)
        error = FriendError.INVALID_REQUEST(
            user_id=self.player_id, request_sender=None
        )
        self.assertEquals(resp.data['error_code'], error.CODE)
        self.assertEquals(resp.data['error_message'], error.message)

    def test_reply_missing_status(self):
        self._create_request()
        resp = self.client.post(settings.URL_PREFIX('/friend/reply/'),
                                data={'request_sender': self.player_id})
        self.assertEquals(resp.status_code, 200)
        error = FriendError.INVALID_STATUS(
            user_id=self.player_id, status=None
        )
        self.assertEquals(resp.data['error_code'], error.CODE)
        self.assertEquals(resp.data['error_message'], error.message)

    def test_reply_no_such_request(self):
        resp = self.client.post(settings.URL_PREFIX('/friend/reply/'),
                                data={'request_sender': -1,
                                      'status': settings.ACCEPTED})
        self.assertEquals(resp.status_code, 200)
        error = FriendError.NO_SUCH_REQUEST(
            user_id=self.player_id, request_sender=-1
        )
        self.assertEquals(resp.data['error_code'], error.CODE)
        self.assertEquals(resp.data['error_message'], error.message)

    def test_reply_already_replied(self):
        self._create_request(replied=True)
        resp = self.client.post(settings.URL_PREFIX('/friend/reply/'),
                                data={'request_sender': self.friend.id,
                                      'status': settings.ACCEPTED})
        self.assertEquals(resp.status_code, 200)
        error = FriendError.ALREADY_REPLIED(
            user_id=self.player_id, request_sender=self.friend.id
        )
        self.assertEquals(resp.data['error_code'], error.CODE)
        self.assertEquals(resp.data['error_message'], error.message)

    def test_break_friendship(self):
        self._create_friendship()
        resp = self.client.post(settings.URL_PREFIX('/friend/break/'),
                                data={'friend_id': self.friend.id})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['player_id'], self.player_id)
        self.assertEquals(resp.data['friend_id'], self.friend.id)
        self.assertIsNotNone(resp.data['break_time'])

    def test_break_missing_friend_id(self):
        self._create_friendship()
        resp = self.client.post(settings.URL_PREFIX('/friend/break/'))
        self.assertEquals(resp.status_code, 200)
        error = FriendError.INVALID_FRIEND(
            user_id=self.player_id, friend_id=None
        )
        self.assertEquals(resp.data['error_code'], error.CODE)
        self.assertEquals(resp.data['error_message'], error.message)

    def test_break_not_friend(self):
        resp = self.client.post(settings.URL_PREFIX('/friend/break/'),
                                data={'friend_id': self.friend.id})
        self.assertEquals(resp.status_code, 200)
        error = FriendError.NOT_FRIEND(
            user_id=self.player_id, player_id=self.friend.id
        )
        self.assertEquals(resp.data['error_code'], error.CODE)
        self.assertEquals(resp.data['error_message'], error.message)


class ModelTest(TestCase):

    def setUp(self):
        self.player_a = Player()
        self.player_a.save()

        self.player_b = Player()
        self.player_b.save()

        self.player_c = Player()
        self.player_c.save()

    def tearDown(self):
        models.Friendship.objects.all().delete()
        models.FriendshipRequestLog.objects.all().delete()

    def test_friendship(self):
        fs = models.Friendship()
        fs.player = self.player_a
        fs.friend = self.player_b
        self.assertIsNone(fs.save())

    def test_friendship_two(self):
        self.test_friendship()
        fs = models.Friendship()
        fs.player = self.player_a
        fs.friend = self.player_c
        self.assertIsNone(fs.save())

    def test_friendship_three(self):
        self.test_friendship_two()
        fs = models.Friendship()
        fs.player = self.player_b
        fs.friend = self.player_c
        self.assertIsNone(fs.save())

    def test_request(self):
        req = models.FriendshipRequestLog()
        req.user_id = self.player_a.id
        req.target_user_id = self.player_b.id
        self.assertIsNone(req.save())

    def test_request_again(self):
        self.test_request()
        req = models.FriendshipRequestLog()
        req.user_id = self.player_a.id
        req.target_user_id = self.player_b.id
        self.assertIsNone(req.save())

        logs = models.FriendshipRequestLog.objects.filter(
            user_id=self.player_a.id, target_user_id=self.player_b.id
        )
        self.assertEquals(len(logs), 2)

    def test_request_two(self):
        self.test_request()
        req = models.FriendshipRequestLog()
        req.user_id = self.player_a.id
        req.target_user_id = self.player_c.id
        self.assertIsNone(req.save())

    def test_break(self):
        log = models.FriendshipBreakLog()
        log.user_id = self.player_a.id
        log.friend_user_id = self.player_b.id
        self.assertIsNone(log.save())

    def test_break_again(self):
        self.test_break()
        log = models.FriendshipBreakLog()
        log.user_id = self.player_a.id
        log.friend_user_id = self.player_b.id
        self.assertIsNone(log.save())
