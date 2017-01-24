from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import (ObjectDoesNotExist, MultipleObjectsReturned)

from django.conf import settings

import go.logging
from card.lobby.apps.player.models import Player
from card.lobby.aop import cache_ysdk_by_user_id, cache_ysdk_by_open_id, args_limit
from card.core.error.lobby import YsdkError

@go.logging.class_wrapper
class Ysdk(models.Model):
    player = models.OneToOneField(Player, primary_key=True, db_column='user_id', verbose_name=_('player'))
    open_id = models.CharField(unique=True, verbose_name=_('open_id'), db_index=True, max_length=120)
    open_key = models.CharField(max_length=120, null=True)
    pf = models.CharField(max_length=50, null=True)
    account_type = models.CharField(max_length=50, null=True)


    def __unicode__(self):
        return self.player.nick_name

    @staticmethod
    @cache_ysdk_by_open_id
    @args_limit('open_id',)
    def get_ysdk_by_open_id(open_id):
        try:
            return Ysdk.objects.get(open_id=open_id)
        except (ObjectDoesNotExist):
            raise YsdkError.OPEN_ID_NOT_EXIST(open_id=open_id)
        except MultipleObjectsReturned:
            assert False, "MultipleObjectsReturned for [open_id|%s]" %open_id
            raise
        except Exception as ex:
            Ysdk.logger.exception(ex)
            raise

    @staticmethod
    @cache_ysdk_by_user_id
    @args_limit('user_id',)
    def get_ysdk_by_user_id(user_id):
        try:
            return Ysdk.objects.get(pk=user_id)
        except (ObjectDoesNotExist):
            raise YsdkError.USER_ID_NOT_EXIST(user_id=user_id)
        except MultipleObjectsReturned:
            assert False, "MultipleObjectsReturned for [user|%d]" %user_id
            raise
        except Exception as ex:
            Ysdk.logger.exception(ex)
            raise

    class Meta:
        db_table = 'player_ysdk'
        verbose_name = verbose_name_plural = ugettext('ysdk')


@go.logging.class_wrapper
class YsdkLog(models.Model):

    _database = settings.LOGGER_DB

    transtype = models.IntegerField(default=0)
    cporderid = models.CharField(max_length=100, db_index=True)
    transid = models.CharField(max_length=50, null=True, db_index=True)
    appuserid = models.IntegerField(default=0)
    appid = models.CharField(max_length=50, null=True)
    waresid = models.IntegerField(default=0)
    item_id = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    feetype = models.IntegerField(default=0)
    money = models.FloatField(default=0)
    currency = models.CharField(max_length=20, null=True)
    result = models.IntegerField(default=0)
    transtime = models.CharField(max_length=50, null=True)
    cpprivate = models.CharField(max_length=50, null=True)
    paytype = models.IntegerField(default=100)
    channel_id = models.CharField(max_length=50, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    taken_id = models.CharField(max_length=50, null=True)
    url_params = models.CharField(max_length=50, null=True)

    @staticmethod
    def get_ysdk_log_by_transid(cporderid):
        try:
            return YsdkLog.objects.get(cporderid=cporderid)
        except (ObjectDoesNotExist):
            return None
        except MultipleObjectsReturned as ex:
            YsdkLog.logger.exception(ex)
            assert False, "MultipleObjectsReturned for get_ysdk_log_by_transid %s" % transid
            raise
        except Exception as ex:
            YsdkLog.logger.exception(ex)
            raise

    @staticmethod
    def get_by_takenid(taken):
        try:
            return YsdkLog.objects.get(taken_id=taken)
        except (ObjectDoesNotExist):
            return None
        except MultipleObjectsReturned as ex:
            YsdkLog.logger.exception(ex)
            assert False, "MultipleObjectsReturned for get_by_takenid %s" % taken
            raise
        except Exception as ex:
            YsdkLog.logger.exception(ex)
            raise

    class Meta:
        db_table = 'ysdk_charge_log'
        verbose_name = verbose_name_plural = ugettext('ysdk_charge_log')
