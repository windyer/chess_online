from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import (ObjectDoesNotExist, MultipleObjectsReturned)

from django.conf import settings

import go.logging
from card.lobby.apps.player.models import Player
from card.lobby.aop import cache_yuyang_by_user_id,cache_yuyang_by_uid,args_limit
from card.core.error.lobby import YuYangError

@go.logging.class_wrapper
class Yuyang(models.Model):
    player = models.OneToOneField(Player, primary_key=True, db_column='user_id', verbose_name=_('player'))
    uid = models.IntegerField(unique=True, verbose_name=_('uid'), db_index=True)

    def __unicode__(self):
        return self.player.nick_name

    @staticmethod
    @cache_yuyang_by_uid
    @args_limit('uid',)
    def get_yuyang_by_uid(uid):
        try:
            return Yuyang.objects.get(uid=uid)
        except (ObjectDoesNotExist):
            raise YuYangError.UID_NOT_EXIST(uid=uid)
        except MultipleObjectsReturned:
            assert False, "MultipleObjectsReturned for [uid|%d]" %uid
            raise
        except Exception as ex:
            Yuyang.logger.exception(ex)
            raise

    @staticmethod
    @cache_yuyang_by_user_id
    @args_limit('user_id',)
    def get_yuyang_by_user_id(user_id):
        try:
            return Yuyang.objects.get(user_id=user_id)
        except (ObjectDoesNotExist):
            raise YuYangError.USER_ID_NOT_EXIST(user_id=user_id)
        except MultipleObjectsReturned:
            assert False, "MultipleObjectsReturned for [user|%d]" %user_id
            raise
        except Exception as ex:
            Yuyang.logger.exception(ex)
            raise

    class Meta:
        db_table = 'player_yuyang'
        verbose_name = verbose_name_plural = ugettext('yuyang')


@go.logging.class_wrapper
class YuyangLog(models.Model):

    _database = settings.LOGGER_DB

    transtype = models.IntegerField(default=0)
    #cporderid = models.CharField(max_length=100, db_index=True)
    transid = models.CharField(max_length=50, null=True, db_index=True)
    appuserid = models.IntegerField(default=0)
    appid = models.CharField(max_length=50, null=True)
    waresid = models.IntegerField(default=0)
    item_id = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    feetype = models.IntegerField(default=0)
    money = models.FloatField(default=0)
    #currency = models.CharField(max_length=20, null=True)
    result = models.IntegerField(default=0)
    transtime = models.CharField(max_length=50, null=True)
    cpprivate = models.CharField(max_length=50, null=True)
    paytype = models.IntegerField(default=100)
    channel_id = models.CharField(max_length=50, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_yuyang_log_by_transid(transid):
        try:
            return YuyangLog.objects.get(transid=transid)
        except (ObjectDoesNotExist):
            return None
        except MultipleObjectsReturned as ex:
            YuyangLog.logger.exception(ex)
            assert False, "MultipleObjectsReturned for get_yuyang_log_by_transid %s" % transid
            raise
        except Exception as ex:
            YuyangLog.logger.exception(ex)
            raise

    @staticmethod
    def get_by_id(_id):
        try:
            return YuyangLog.objects.get(id=_id)
        except (ObjectDoesNotExist):
            return None
        except MultipleObjectsReturned as ex:
            YuyangLog.logger.exception(ex)
            assert False, "MultipleObjectsReturned for get_by_id %s" % _id
            raise
        except Exception as ex:
            YuyangLog.logger.exception(ex)
            raise

    class Meta:
        db_table = 'yuyang_charge_log'
        verbose_name = verbose_name_plural = ugettext('yuyang_charge_log')
