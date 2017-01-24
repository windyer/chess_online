from django.db import models
from django.utils.translation import ugettext

from django.conf import settings

class TurnerLog(models.Model):
    _database = settings.LOGGER_DB
    
    user_id = models.PositiveIntegerField()
    award_currency = models.PositiveIntegerField()
    cost = models.PositiveIntegerField()
    round = models.PositiveIntegerField()
    win_or_lose = models.CharField(max_length=20)
    created_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'{0}, {1}'.format(self.user_id, self.win_or_lose)

    class Meta:
        db_table = 'turner_log'
        verbose_name = verbose_name_plural = ugettext('turner_log')
