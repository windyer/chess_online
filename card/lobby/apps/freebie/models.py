from django.db import models
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import (ObjectDoesNotExist, MultipleObjectsReturned)

from django.conf import settings

import go.logging

@go.logging.class_wrapper
class YoumiWallLog(models.Model):

    _database = settings.LOGGER_DB
    
    platform = models.CharField(max_length=20)
    order = models.CharField(max_length=100)
    app = models.CharField(max_length=100)
    ad = models.CharField(max_length=100)
    adid = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    device = models.CharField(max_length=100)
    chn = models.IntegerField()
    price = models.FloatField()
    points = models.IntegerField()
    time = models.IntegerField()
    sig = models.CharField(max_length=100)
    sign = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_score_wall_log(order_id):
        try:
            return YoumiWallLog.objects.get(order=order_id)
        except (ObjectDoesNotExist):
            return None
        except MultipleObjectsReturned:
            assert False, "MultipleObjectsReturned for get_score_wall_log %s" % order_id
            raise
        except Exception as ex:
            YoumiWallLog.logger.exception(ex)
            raise

    class Meta:
        db_table = 'freebie_youmi_wall_log'
        verbose_name = verbose_name_plural = ugettext('youmi_wall_log')

@go.logging.class_wrapper
class ScoreWallLog(models.Model):

    _database = settings.LOGGER_DB
    
    user_id = models.IntegerField()
    order_id = models.CharField(max_length=100)
    vender = models.CharField(max_length=20)
    score = models.IntegerField()
    sign = models.CharField(max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_score_wall_log(order_id):
        try:
            return ScoreWallLog.objects.get(order_id=order_id)
        except (ObjectDoesNotExist):
            return None
        except MultipleObjectsReturned:
            assert False, "MultipleObjectsReturned for get_score_wall_log %s" % order_id
            raise
        except Exception as ex:
            ScoreWallLog.logger.exception(ex)
            raise

    class Meta:
        db_table = 'freebie_score_wall_log'
        verbose_name = verbose_name_plural = ugettext('score_wall_log')