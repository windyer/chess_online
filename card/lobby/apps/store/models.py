from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from django.conf import settings

from card.lobby.apps.player.models import Player

from card.core.enum.items import ITEM_NAMES


class PlayerProperty(models.Model):
    player = models.OneToOneField(Player, primary_key=True, db_column='user_id', related_name="property", verbose_name=_('player'))
    rabbit_girl = models.PositiveIntegerField(verbose_name=_('rabbit_girl'), default=0)
    roses = models.PositiveIntegerField(verbose_name=_('roses'), default=0)
    ship = models.PositiveIntegerField(verbose_name=_('ship'), default=0)
    car = models.PositiveIntegerField(verbose_name=_('car'), default=0)
    rose = models.PositiveIntegerField(verbose_name=_('rose'), default=0)
    cigar = models.PositiveIntegerField(verbose_name=_('cigar'), default=0)
    red_wine = models.PositiveIntegerField(verbose_name=_('red_wine'), default=0)
    kick_seat_card = models.PositiveIntegerField(verbose_name=_('kick_seat_card'), default=0)
    avoid_kick_card = models.PositiveIntegerField(verbose_name=_('avoid_kick_card'), default=0)
    speaker = models.PositiveIntegerField(verbose_name=_('speaker'), default=0)
    replace_card = models.PositiveIntegerField(verbose_name=_('replace_card'), default=0)
    bad_egg = models.PositiveIntegerField(verbose_name=_('bad_egg'), default=0)
    name_card = models.PositiveIntegerField(verbose_name=_('name_card'), default=0)
    turner_card = models.PositiveIntegerField(verbose_name=_('turner_card'), default=0)
    soap = models.PositiveIntegerField(verbose_name=_('soap'), default=0)
    daily_speaker = models.PositiveIntegerField(verbose_name=_('daily_speaker'), default=0)
    lottery_ticket = models.PositiveIntegerField(verbose_name=_('lottery_ticket'), default=0)

    def __unicode__(self):
        return u'<{0}, {1}>'.format(self.player.nick_name, self.player.user_id)

    class Meta:
        db_table        = 'player_property'
        verbose_name    = verbose_name_plural = ugettext('player_property')

class StorePurchaseLog(models.Model):
    _database = settings.LOGGER_DB

    user_id = models.PositiveIntegerField()
    item_id = models.PositiveIntegerField(choices=ITEM_NAMES)
    count   = models.PositiveIntegerField()
    cost    = models.PositiveIntegerField()

    class Meta:
        db_table = 'store_purchase_log'


class StoreSellLog(models.Model):
    _database = settings.LOGGER_DB
    
    user_id = models.PositiveIntegerField()
    item_id = models.PositiveIntegerField(choices=ITEM_NAMES)
    count   = models.PositiveIntegerField()
    earn    = models.PositiveIntegerField()

    class Meta:
        db_table = 'store_sell_log'
