from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import (ObjectDoesNotExist, MultipleObjectsReturned)

from django.conf import settings

import go.logging
from card.lobby.apps.player.models import Player
from card.lobby.aop import cache_dianyou_by_uid,cache_dianyou_by_user_id,args_limit
from card.core.error.lobby import DianyouError

@go.logging.class_wrapper
class Dianyou(models.Model):
    player = models.OneToOneField(Player, primary_key=True, db_column='user_id', verbose_name=_('player'))
    uid = models.IntegerField(unique=True, verbose_name=_('uid'), db_index=True)

    def __unicode__(self):
        return self.player.nick_name

    @staticmethod
    @cache_dianyou_by_uid
    @args_limit('uid',)
    def get_dianyou_by_uid(uid):
        try:
            return Dianyou.objects.get(uid=uid)
        except (ObjectDoesNotExist):
            raise DianyouError.UID_NOT_EXIST(uid=uid)
        except MultipleObjectsReturned:
            assert False, "MultipleObjectsReturned for [uid|%d]" %uid
            raise
        except Exception as ex:
            Dianyou.logger.exception(ex)
            raise

    @staticmethod
    @cache_dianyou_by_user_id
    @args_limit('user_id',)
    def get_dianyou_by_user_id(user_id):
        try:
            return Dianyou.objects.get(user_id=user_id)
        except (ObjectDoesNotExist):
            raise DianyouError.USER_ID_NOT_EXIST(user_id=user_id)
        except MultipleObjectsReturned:
            assert False, "MultipleObjectsReturned for [user|%d]" %user_id
            raise
        except Exception as ex:
            Dianyou.logger.exception(ex)
            raise

    class Meta:
        db_table = 'player_dianyou'
        verbose_name = verbose_name_plural = ugettext('dianyou')


@go.logging.class_wrapper
class DianyouLog(models.Model):

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
    def get_dianyou_log_by_transid(transid):
        try:
            return DianyouLog.objects.get(transid=transid)
        except (ObjectDoesNotExist):
            return None
        except MultipleObjectsReturned as ex:
            DianyouLog.logger.exception(ex)
            assert False, "MultipleObjectsReturned for get_dianyou_log_by_transid %s" % transid
            raise
        except Exception as ex:
            DianyouLog.logger.exception(ex)
            raise

    @staticmethod
    def get_by_id(_id):
        try:
            return DianyouLog.objects.get(id=_id)
        except (ObjectDoesNotExist):
            return None
        except MultipleObjectsReturned as ex:
            DianyouLog.logger.exception(ex)
            assert False, "MultipleObjectsReturned for get_by_id %s" % _id
            raise
        except Exception as ex:
            DianyouLog.logger.exception(ex)
            raise

    class Meta:
        db_table = 'dianyou_charge_log'
        verbose_name = verbose_name_plural = ugettext('dianyou_charge_log')
