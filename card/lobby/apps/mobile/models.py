from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import (ObjectDoesNotExist, MultipleObjectsReturned)

from django.conf import settings
from card.core.enum.items import ITEM_NAMES

import go.logging

@go.logging.class_wrapper
class MobileLog(models.Model):

    _database = settings.LOGGER_DB
    
    OrderID = models.CharField(max_length=40, db_index=True)
    user_id = models.IntegerField()
    item_id = models.IntegerField(choices=ITEM_NAMES)
    CheckID = models.IntegerField(null=True)
    TradeID = models.CharField(max_length=70, null=True)
    Price = models.IntegerField(null=True)
    ActionTime = models.CharField(max_length=20)
    ActionID = models.IntegerField()
    MSISDN = models.CharField(max_length=20, null=True)
    FeeMSISDN = models.CharField(max_length=40, null=True)
    AppID = models.CharField(max_length=30)
    ProgramID = models.CharField(max_length=30, null=True)
    PayCode = models.CharField(max_length=30, null=True)
    TotalPrice = models.IntegerField(null=True)
    SubsNumb = models.IntegerField(null=True)
    SubsSeq = models.IntegerField(null=True)
    ChannelID = models.CharField(max_length=70, null=True)
    OrderType = models.IntegerField(null=True)
    OrderPayment = models.IntegerField()
    MD5Sign = models.CharField(max_length=32)
    created_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_mobile_log(OrderID):
        try:
            return MobileLog.objects.get(OrderID=OrderID)
        except (ObjectDoesNotExist):
            return None
        except MultipleObjectsReturned as ex:
            MobileLog.logger.exception(ex)
            assert False, "MultipleObjectsReturned for get_mobile_log %s" % OrderID
            raise
        except Exception as ex:
            MobileLog.logger.exception(ex)
            raise

    class Meta:
        db_table = 'mobile_charge_log'
        verbose_name = verbose_name_plural = ugettext('mobile_charge_log')







