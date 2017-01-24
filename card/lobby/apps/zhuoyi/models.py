from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import (ObjectDoesNotExist, MultipleObjectsReturned)

from django.conf import settings

import go.logging

@go.logging.class_wrapper
class ZhuoyiLog(models.Model):

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
    result = models.IntegerField(default=100)
    transtime = models.CharField(max_length=50, null=True)
    cpprivate = models.CharField(max_length=50, null=True)
    paytype = models.IntegerField(default=100)
    channel_id = models.CharField(max_length=50, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_zhuoyi_log_by_orderid(order_id):
        try:
            return ZhuoyiLog.objects.get(cporderid=order_id)
        except (ObjectDoesNotExist):
            return None
        except MultipleObjectsReturned as ex:
            ZhuoyiLog.logger.exception(ex)
            assert False, "MultipleObjectsReturned for get_zhuoyi_log_by_cporderid %s" % order_id
            raise
        except Exception as ex:
            ZhuoyiLog.logger.exception(ex)
            raise

    @staticmethod
    def get_zhuoyi_log_by_transid(transid):
        try:
            return ZhuoyiLog.objects.get(transid=transid)
        except (ObjectDoesNotExist):
            return None
        except MultipleObjectsReturned as ex:
            ZhuoyiLog.logger.exception(ex)
            assert False, "MultipleObjectsReturned for get_zhuoyi_log_by_transid %s" % transid
            raise
        except Exception as ex:
            ZhuoyiLog.logger.exception(ex)
            raise

    class Meta:
        db_table = 'zhuoyi_charge_log'
        verbose_name = verbose_name_plural = ugettext('zhuoyi_charge_log')
