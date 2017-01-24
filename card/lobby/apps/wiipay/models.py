from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import (ObjectDoesNotExist, MultipleObjectsReturned)

from django.conf import settings

import go.logging
from card.lobby.apps.player.models import Player

@go.logging.class_wrapper
class WiipayLog(models.Model):

    _database = settings.LOGGER_DB

    operator_type = models.CharField(max_length=50, null=True)
    cporderid = models.CharField(max_length=100, db_index=True)
    transid = models.CharField(max_length=50, null=True, db_index=True)
    appuserid = models.IntegerField(default=0)
    appid = models.CharField(max_length=50, null=True)
    waresid = models.IntegerField(default=0)
    item_id = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    money = models.FloatField(default=0)
    result = models.IntegerField(default=100)
    transtime = models.CharField(max_length=50, null=True)
    channel_id = models.CharField(max_length=50, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    syn_type = models.CharField(max_length=50, null=True)
    channel_code = models.CharField(max_length=500, null=True)
    app_code = models.CharField(max_length=500, null=True)
    pay_code = models.CharField(max_length=500, null=True)

    @staticmethod
    def get_wiipay_log_by_cporderid(order_id):
        try:
            return WiipayLog.objects.get(cporderid=order_id)
        except (ObjectDoesNotExist):
            return None
        except MultipleObjectsReturned as ex:
            WiipayLog.logger.exception(ex)
            assert False, "MultipleObjectsReturned for get_wiipay_log_by_cporderid %s" % order_id
            raise
        except Exception as ex:
            WiipayLog.logger.exception(ex)
            raise

    @staticmethod
    def get_wiipay_log_by_transid(transid):
        try:
            return WiipayLog.objects.get(transid=transid)
        except (ObjectDoesNotExist):
            return None
        except MultipleObjectsReturned as ex:
            WiipayLog.logger.exception(ex)
            assert False, "MultipleObjectsReturned for get_wiipay_log_by_transid %s" % transid
            raise
        except Exception as ex:
            WiipayLog.logger.exception(ex)
            raise

    class Meta:
        db_table = 'wiipay_charge_log'
        verbose_name = verbose_name_plural = ugettext('wiipay_charge_log')