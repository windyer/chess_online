from django.db import models
from django.db import IntegrityError
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import (ObjectDoesNotExist, MultipleObjectsReturned)

from django.conf import settings

import go.logging

from card.core.error.lobby import HolyTreeError
from card.lobby.apps.player.models import Player
from card.lobby.apps.holytree.redis import HolyTreeUserId, HolyTreeUserName
from card.lobby.aop import (cache_holytree_by_user_name, cache_guest_by_device_id,
                            cache_holytree_by_user_id, args_limit, cache_guest_by_user_id)


class CreatePolicy(models.Model):
    create_key = models.CharField(unique=True, verbose_name=_('create_key'), db_index=True, max_length=100)

    @staticmethod
    def create_account(create_key):
        try:
            user = CreatePolicy()
            user.create_key = create_key
            user.save()
        except IntegrityError:
            raise HolyTreeError.USER_NAME_ALREADY_EXIST(user_name=create_key)

    @staticmethod
    def delete_account(create_key):
        try:
            mysql_object = CreatePolicy.objects.get(create_key=create_key)
            mysql_object.delete()
        except CreatePolicy.DoesNotExist:
            pass

    def __unicode__(self):
        return u'<{0}>'.format(self.create_key)

    class Meta:
        db_table = 'create_policy'
        verbose_name = verbose_name_plural = ugettext('create_policy')

@go.logging.class_wrapper
class Guest(models.Model):
    player = models.OneToOneField(Player, primary_key=True, db_column='user_id', verbose_name=_('player'))
    device_id = models.CharField(max_length=32, unique=True, db_index=True, verbose_name=_('device_id'),)

    def __unicode__(self):
        return u'<{0}-{1}>'.format(self.player.user_id, self.player.nick_name)

    @staticmethod
    @cache_guest_by_device_id
    @args_limit('device_id',)
    def get_guest_by_device_id(device_id):
        try:
            return Guest.objects.get(device_id=device_id)
        except (ObjectDoesNotExist):
            raise HolyTreeError.USER_NAME_NOT_EXIST(user_name=device_id)
        except MultipleObjectsReturned:
            assert False, "MultipleObjectsReturned for [user_name|%d]" %user_name
            raise
        except Exception as ex:
            Guest.logger.exception(ex)
            raise

    @staticmethod
    @cache_guest_by_user_id
    @args_limit('user_id',)
    def get_guest_by_user_id(user_id):
        try:
            return Guest.objects.get(pk=user_id)
        except (ObjectDoesNotExist):
            raise HolyTreeError.USER_ID_NOT_EXIST(user_id=user_id)
        except MultipleObjectsReturned:
            assert False, "MultipleObjectsReturned for [user|%d]" %user_id
            raise
        except Exception as ex:
            Guest.logger.exception(ex)
            raise

    @staticmethod
    def delete_guest(rguest):
        device_id = rguest.device_id
        user_id = rguest.user_id
        rguest.delete()
        guest = Guest.get_guest_by_device_id(device_id=device_id)
        guest.delete()

        mysql_object = Guest.objects.get(pk=user_id)
        mysql_object.delete()
        
        CreatePolicy.delete_account(device_id)

    class Meta:
        db_table = 'player_guest'
        verbose_name = verbose_name_plural = ugettext('guest')


class Robot(models.Model):
    player = models.OneToOneField(Player, primary_key=True, db_column='user_id', verbose_name=_('player'))
    token = models.CharField(max_length=40, unique=True, verbose_name=_('token'),)

    def __unicode__(self):
        return u'<{0}-{1}>'.format(self.player.user_id, self.player.nick_name)

    class Meta:
        db_table = 'player_robot'
        verbose_name = verbose_name_plural = ugettext('robot')

@go.logging.class_wrapper
class HolyTree(models.Model):
    player = models.OneToOneField(Player, primary_key=True, db_column='user_id', verbose_name=_('player'))
    user_name = models.CharField(unique=True, verbose_name=_('user_name'), db_index=True, max_length=100)
    password = models.CharField(unique=False, verbose_name=_('password'), db_index=False, max_length=100)
    
    def __unicode__(self):
        return self.player.nick_name

    @staticmethod
    @cache_holytree_by_user_id
    @args_limit('user_id',)
    def get_holytree_by_user_id(user_id):
        try:
            return HolyTree.objects.get(pk=user_id)
        except (ObjectDoesNotExist):
            raise HolyTreeError.USER_ID_NOT_EXIST(user_id=user_id)
        except MultipleObjectsReturned:
            assert False, "MultipleObjectsReturned for [user|%d]" %user_id
            raise
        except Exception as ex:
            HolyTree.logger.exception(ex)
            raise

    @staticmethod
    @cache_holytree_by_user_name
    @args_limit('user_name',)
    def get_holytree_by_user_name(user_name):
        try:
            return HolyTree.objects.get(user_name=user_name)
        except (ObjectDoesNotExist):
            raise HolyTreeError.USER_NAME_NOT_EXIST(user_name=user_name)
        except MultipleObjectsReturned:
            assert False, "MultipleObjectsReturned for [user_name|%d]" %user_name
            raise
        except Exception as ex:
            HolyTree.logger.exception(ex)
            raise

    @staticmethod
    def update_password(user_id, password):
        try:
            mysql_object = HolyTree.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            raise HolyTreeError.USER_ID_NOT_EXIST(user_id=user_id)
        except MultipleObjectsReturned:
            raise
        except Exception as ex:
            raise

        mysql_object.password = password
        mysql_object.save()

        user_name = mysql_object.user_name
        user_name = user_name.strip()
        user_name = user_name.lower()

        rholytree = HolyTreeUserName()
        rholytree.set_id(user_name)
        rholytree.user_id = mysql_object.player.user_id
        rholytree.user_name = mysql_object.user_name
        rholytree.password = password
        rholytree.save()

        rholytree = HolyTreeUserId()
        rholytree.set_id(mysql_object.player.user_id)
        rholytree.user_id = mysql_object.player.user_id
        rholytree.user_name = mysql_object.user_name
        rholytree.password = password
        rholytree.save()

    class Meta:
        db_table = 'player_holytree'
        verbose_name = verbose_name_plural = ugettext('holytree')
