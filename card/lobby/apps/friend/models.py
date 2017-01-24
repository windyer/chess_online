from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings


from card.core.enum.items import ITEM_NAMES
STATUS_CHOICES = (
    (settings.ACCEPTED, settings.ACCEPTED),
    (settings.DECLINED, settings.DECLINED),
)

class Friendship(models.Model):
    user_id = models.PositiveIntegerField()
    friend_id = models.PositiveIntegerField()
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('make_friendship_time'))

    class Meta:
        unique_together = ("user_id", "friend_id")
        db_table = 'friendship'
        verbose_name = verbose_name_plural = ugettext('friendship')

    def __unicode__(self):
        return u'<{0}, {1}>'.format(self.user_id, self.friend_id)


class FriendshipRequestLog(models.Model):
    _database = settings.LOGGER_DB

    user_id = models.PositiveIntegerField()
    target_user_id = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=settings.PENDING, verbose_name=_('status'))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('requested_time'))
    replied_time = models.DateTimeField(null=True, blank=True, verbose_name=_('replied_time'))
    gift_id = models.IntegerField(null=True, verbose_name=_('gift'))

    class Meta:
        db_table = 'friendship_request_log'
        verbose_name = verbose_name_plural = ugettext('friendship_request_log')

    def __unicode__(self):
        return u'<{0}, {1}>'.format(self.user_id,
                self.target_user_id)

class FriendshipBreakLog(models.Model):
    _database = settings.LOGGER_DB

    user_id = models.PositiveIntegerField()
    friend_user_id = models.PositiveIntegerField()
    break_time = models.DateTimeField(auto_now_add=True, verbose_name=_('break_time'))

    class Meta:
        db_table = 'friendship_break_log'
        verbose_name = verbose_name_plural = ugettext('friendship_break_log')


class SendCurrencyLog(models.Model):
    _database = settings.LOGGER_DB

    user_id = models.PositiveIntegerField()
    target_user_id = models.PositiveIntegerField()
    currency = models.BigIntegerField()
    commission = models.FloatField()
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'friendship_currency_log'

    def __unicode__(self):
        return u'<{0}, {1}, {2}>'.format(self.user_id,
                self.target_user_id, self.currency)


class SendGiftLog(models.Model):
    _database = settings.LOGGER_DB
    
    user_id        = models.PositiveIntegerField()
    target_user_id = models.PositiveIntegerField()
    item_id        = models.IntegerField(choices=ITEM_NAMES)
    count          = models.IntegerField()
    created_time   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'friendship_gift_log'

    def __unicode__(self):
        return u'<{0}, {1}, {2} * {3}>'.format(self.user_id,
                self.target_user_id, self.item_id, self.count)
