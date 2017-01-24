from django.db import models
from django.utils.translation import ugettext

from django.conf import settings

class RouletteLog(models.Model):
    _database = settings.LOGGER_DB
    
    user_id = models.PositiveIntegerField()
    item_id = models.PositiveIntegerField()
    name = models.CharField(max_length=64)
    count = models.PositiveIntegerField()
    cost = models.PositiveIntegerField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'{0}, {1}'.format(self.user_id, self.item_id)

    class Meta:
        db_table = 'roulette_log'
        verbose_name = verbose_name_plural = ugettext('roulette_log')

class RouletteRecord(models.Model):
    user_id = models.PositiveIntegerField(db_index=True)
    item_id = models.PositiveIntegerField()
    item_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'roulette_record'
        verbose_name = verbose_name_plural = ugettext('roulette_record')
