from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import (ObjectDoesNotExist, MultipleObjectsReturned)

from django.conf import settings

import go.logging

@go.logging.class_wrapper
class SkypayLog(models.Model):

    _database = settings.LOGGER_DB
    
    orderId = models.CharField(max_length=100, db_index=True)

    cardType = models.CharField(max_length=20, null=True)
    skyId = models.BigIntegerField()
    resultCode = models.IntegerField(default=100)
    payNum = models.CharField(max_length=60, default="")
    realAmount = models.BigIntegerField(default=0)
    payTime = models.CharField(max_length=20, null=True)
    failure = models.CharField(max_length=20, null=True)
    failDesc = models.CharField(max_length=300, null=True)
    ext1 = models.CharField(max_length=50, null=True)
    ext2 = models.CharField(max_length=50, null=True)
    ext3 = models.CharField(max_length=50, null=True)
    signMsg = models.CharField(max_length=40, null=True)

    payMethod = models.CharField(max_length=20)
    price = models.IntegerField()
    systemId = models.IntegerField()
    payType = models.IntegerField()
    appVersion = models.IntegerField()
    channelId = models.CharField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_skypay_log(order_id):
        try:
            return SkypayLog.objects.get(orderId=order_id)
        except (ObjectDoesNotExist):
            return None
        except MultipleObjectsReturned as ex:
            SkypayLog.logger.exception(ex)
            assert False, "MultipleObjectsReturned for get_skypay_log %s" % order_id
            raise
        except Exception as ex:
            SkypayLog.logger.exception(ex)
            raise

    class Meta:
        db_table = 'skypay_charge_log'
        verbose_name = verbose_name_plural = ugettext('skypay_charge_log')
