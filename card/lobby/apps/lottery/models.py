from django.db import models
from django.utils.translation import ugettext

from django.conf import settings

class LotteryRecord(models.Model):
    user_id = models.PositiveIntegerField(db_index=True)
    item_id = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    number = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField()
    gm_name = models.CharField(max_length=64)
    handle_time = models.DateTimeField()
    handle_sn = models.CharField(max_length=64)

    class Meta:
        db_table = 'lottery_record'
        verbose_name = verbose_name_plural = ugettext('lottery_record')
