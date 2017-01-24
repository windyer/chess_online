import random

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import (ObjectDoesNotExist, MultipleObjectsReturned)

from card.core.conf import settings
from card.core.enum import (Gender, Platform, Vip)
from card.core.error.lobby import PlayerError
from card.lobby.aop import cache_player_extra

class SessionPlayer(object):

    def __init__(self, user_id):
        self._user_id = user_id

    @property
    def id(self):
        return self._user_id
    pk = id

    @property
    def is_active(self):
        return True

    @property
    def is_staff(self):
        return False

    def is_authenticated(self):
        return True

    def save(self, *args, **kwargs):
        pass

    def __unicode__(self):
        return u'<SessionPlayer:%d>' % self.id
    __str__ = __unicode__


class Player(models.Model):

    GENDERS = (
        (Gender.MALE, _('male')),
        (Gender.FEMALE, _('female')),
        (Gender.UNKNOWN, _('unknown')),
    )
    
    user_id = models.IntegerField(primary_key=True)
    nick_name = models.CharField(max_length=100, verbose_name=_('nick_name'))
    age = models.PositiveIntegerField(default=0, verbose_name=_('age'))
    gender = models.IntegerField(verbose_name=_('gender'), choices=GENDERS, default=Gender.UNKNOWN)
    avatar_url = models.CharField(max_length=100, blank=True, verbose_name=_('avatar_url'))
    currency = models.BigIntegerField(default=0, verbose_name=_('currency'))
    cat_weight = models.BigIntegerField(default=0, verbose_name=_('cat_weight'))
    bank_currency = models.BigIntegerField(default=0, verbose_name=_('bank_currency'))
    charge_times = models.BigIntegerField(default=0, verbose_name=_('charge_times'))
    charge_money = models.BigIntegerField(default=0, verbose_name=_('charge_money'))
    last_charge_time = models.BigIntegerField(default=0, verbose_name=_('last_charge_time'))
    is_robot = models.BooleanField(default=False, verbose_name=_('is_robot'))
    is_listener = models.BooleanField(default=False, verbose_name=_('is_listener'))
    is_active = models.BooleanField(default=True, verbose_name=_('is_active'))
    channel = models.CharField(max_length=50, verbose_name=_('channel'), null=True)
    mute_end_time = models.BigIntegerField(default=0, verbose_name=_('mute_end_time'))
    is_monthly_player = models.BooleanField(default=False, verbose_name=_('is_monthly_player'))

    @staticmethod
    def get_player(user_id):
        try:
            return Player.objects.get(pk=user_id)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            raise
        except Exception:
            raise

    def new_id(self):
        '''
            only new create player can use this method
        '''
        begin_id = 1000003
        prime_numbers = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
        try:
            max_id = Player.objects.latest('user_id').user_id
        except Player.DoesNotExist:
            max_id = begin_id
        if max_id < begin_id:
            max_id = begin_id
        delta = random.choice(prime_numbers)
        return max_id + delta

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self.new_id()
        return super(Player, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'<%d-%s>' % (self.user_id, self.nick_name)

    class Meta:
        db_table = 'player'
        verbose_name = verbose_name_plural = ugettext('player')


class PlayerProfile(models.Model):
    player = models.OneToOneField(Player, primary_key=True, db_column='user_id', related_name='profile', verbose_name=_('profile'))
    round_max_win = models.PositiveIntegerField(default=0, verbose_name=_('round_max_win'))
    total_max_currency = models.BigIntegerField(default=0, verbose_name=_('total_max_currency'))
    total_rounds = models.PositiveIntegerField(default=0, verbose_name=_('total_rounds'))
    total_win_rounds = models.PositiveIntegerField(default=0, verbose_name=_('total_win_rounds'))
    total_lose_rounds = models.PositiveIntegerField(default=0, verbose_name=_('total_lose_rounds'))
    max_hand_card = models.CharField(max_length=60, null=True, verbose_name=_('max_hand_card'))
    signature = models.CharField(max_length=100, verbose_name=_('signature'), null=True)
    contact = models.CharField(max_length=100, verbose_name=_('contact'), null=True)

    def __unicode__(self):
        return u'<{0}-{1}>'.format(self.player.user_id, self.player.nick_name)

    class Meta:
        db_table = 'player_profile'
        verbose_name = verbose_name_plural = ugettext('player_profile')

class PlayerExtra(models.Model):
    PLAYER_TYPES = (
        (Platform.GUEST, _('guest')),
        (Platform.ROBOT, _('robot')),
        (Platform.HOLYTREE, _('holytree')),
    )

    player = models.OneToOneField(Player, primary_key=True, db_column='user_id', related_name='extra', verbose_name=_('extra'))
    player_type = models.IntegerField(verbose_name=_('player_type'), choices=PLAYER_TYPES)
    login_ip = models.CharField(max_length=20, verbose_name=_('login_ip'), null=True)
    login_device_id = models.CharField(max_length=32, verbose_name=_('login_device_id'), null=True)
    last_login_time = models.DateTimeField(verbose_name=_('last_login_time'), null=True)
    continuous_login_days = models.PositiveIntegerField(default=0, verbose_name=_('continuous_login_days'))
    app_version = models.CharField(max_length=20, verbose_name=_('app_version'), null=True)
    package_type = models.CharField(max_length=20, verbose_name=_('package_type'), null=True)
    os_version = models.CharField(max_length=50, verbose_name=_('os_version'), null=True)
    os_platform = models.CharField(max_length=50, verbose_name=_('os_platform'), null=True)
    channel = models.CharField(max_length=50, verbose_name=_('channel'), null=True)
    vip_award_steps = models.CharField(max_length=100, verbose_name=_('vip_award_steps'), null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('created_time'))
    created_device_id = models.CharField(max_length=32, verbose_name=_('created_device_id'))
    token = models.CharField(max_length=32, null=True, verbose_name=_('token'))
    monthly_payment = models.BooleanField(default=False, verbose_name=_('monthly_payment'))
    monthly_pay_time = models.BigIntegerField(default=0, verbose_name=_('monthly_pay_time'))
    monthly_unsubscribe_time = models.BigIntegerField(default=0, verbose_name=_('monthly_unsubscribe_time'))
    monthly_continuous = models.BooleanField(default=False, verbose_name=_('monthly_continuous'))
    monthly_end_time = models.BigIntegerField(default=0, verbose_name=_('monthly_end_time'))
    monthly_mature_end = models.BooleanField(default=False, verbose_name=_('monthly_mature_end'))
    vender = models.CharField(max_length=32, verbose_name=_('vender'), null=True)
    networking = models.CharField(max_length=32, verbose_name=_('networking'), null=True)
    resolution = models.CharField(max_length=32, verbose_name=_('resolution'), null=True)
    imei_number = models.CharField(max_length=32, verbose_name=_('imei_number'), null=True)
    last_identify_time = models.DateTimeField(verbose_name=_('last_identify_time'), null=True)
    bank_password = models.CharField(max_length=32, verbose_name=_('bank_password'))

    @staticmethod
    @cache_player_extra
    def get_player_extra(user_id):
        try:
            return PlayerExtra.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            raise PlayerError.PLAYER_NOT_EXISTS(user_id=user_id)
        except MultipleObjectsReturned:
            raise
        except Exception:
            raise

    @staticmethod
    def update_player_extra(player_extra):
        try:
            mysql_object = PlayerExtra.objects.get(pk=player_extra.user_id)
        except ObjectDoesNotExist:
            raise PlayerError.PLAYER_NOT_EXISTS(user_id=player_extra.user_id)
        except MultipleObjectsReturned:
            raise
        except Exception as ex:
            raise

        for field in player_extra.fields().values():
            value = getattr(player_extra, field.name, field.default)
            setattr(mysql_object, field.name, value)

        try:
            mysql_object.save()
            assert player_extra.is_valid()
            save_resp = player_extra.save()
            assert save_resp == True
        except Exception as ex:
            raise ex

    def __unicode__(self):
        return u'<{0}-{1}>'.format(self.player.user_id, self.player.nick_name)

    class Meta:
        db_table = 'player_extra'
        verbose_name = verbose_name_plural = ugettext('player_extra')

class ReportLog(models.Model):
    _database = settings.LOGGER_DB

    user_id = models.PositiveIntegerField()
    target_user_id = models.PositiveIntegerField()
    reason = models.CharField(max_length=50, null=True, verbose_name=_('reason'))
    context = models.CharField(max_length=500, null=True, verbose_name=_('context'))
    is_processed = models.BooleanField(default=False, verbose_name=_('is_processed'))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('report_time'))

    class Meta:
        db_table = 'report_log'
        verbose_name = verbose_name_plural = ugettext('report_log')

    def __unicode__(self):
        return u'<{0}, {1}>'.format(self.user_id, self.target_user_id)

class PlayerThree(models.Model):
    player = models.OneToOneField(Player, primary_key=True, db_column='user_id', related_name='three', verbose_name=_('three'))
    three_total_dealer_rounds = models.BigIntegerField(default=0, verbose_name=_('three_total_dealer_rounds'))
    three_total_rounds = models.PositiveIntegerField(default=0, verbose_name=_('three_total_rounds'))
    three_round_max_win = models.BigIntegerField(default=0, verbose_name=_('three_round_max_win'))
    three_total_win = models.BigIntegerField(default=0, verbose_name=_('three_total_win'))
    three_dealer_total_win = models.BigIntegerField(default=0, verbose_name=_('three_dealer_total_win'))
    three_total_lose = models.BigIntegerField(default=0, verbose_name=_('three_total_lose'))
    three_dealer_total_lose = models.BigIntegerField(default=0, verbose_name=_('three_dealer_total_lose'))
    three_total_win_rounds = models.PositiveIntegerField(default=0, verbose_name=_('three_total_win_rounds'))
    three_total_lose_rounds = models.PositiveIntegerField(default=0, verbose_name=_('three_total_lose_rounds'))

    def __unicode__(self):
        return u'<{0}-{1}>'.format(self.player.user_id, self.player.nick_name)

    class Meta:
        db_table = 'player_three'
        verbose_name = verbose_name_plural = ugettext('player_three')

class ThreePool(models.Model):
    three_id = models.IntegerField(primary_key=True)
    pool_currency = models.BigIntegerField(default=0, verbose_name=_('pool_currency'))
    max_win_user_id = models.BigIntegerField(default=0, verbose_name=_('max_win_user_id'))
    max_win_currency = models.PositiveIntegerField(default=0, verbose_name=_('max_win_currency'))
    max_win_nick_name = models.CharField(max_length=100, verbose_name=_('max_win_nick_name'))
    max_win_avatar_url = models.CharField(max_length=100, blank=True, verbose_name=_('max_win_avatar_url'))

    def __unicode__(self):
        return u'<{0}-{1}>'.format(self.three_id, self.pool_currency)

    class Meta:
        db_table = 'three_pool'
        verbose_name = verbose_name_plural = ugettext('three_pool')

class PlayerFruit(models.Model):
    player = models.OneToOneField(Player, primary_key=True, db_column='user_id', related_name='fruit', verbose_name=_('fruit'))
    fruit_total_rounds = models.PositiveIntegerField(default=0, verbose_name=_('fruit_total_rounds'))
    fruit_total_win = models.BigIntegerField(default=0, verbose_name=_('fruit_total_win'))
    fruit_total_lose = models.BigIntegerField(default=0, verbose_name=_('fruit_total_lose'))
    fruit_total_win_rounds = models.PositiveIntegerField(default=0, verbose_name=_('fruit_total_win_rounds'))
    fruit_total_lose_rounds = models.PositiveIntegerField(default=0, verbose_name=_('fruit_total_lose_rounds'))

    def __unicode__(self):
        return u'<{0}-{1}>'.format(self.player.user_id, self.player.nick_name)

    class Meta:
        db_table = 'player_fruit'
        verbose_name = verbose_name_plural = ugettext('player_fruit')

class FruitPool(models.Model):
    fruit_id = models.IntegerField(primary_key=True)
    pool_currency = models.BigIntegerField(default=0, verbose_name=_('pool_currency'))
    max_win_user_id = models.BigIntegerField(default=0, verbose_name=_('max_win_user_id'))
    max_win_currency = models.PositiveIntegerField(default=0, verbose_name=_('max_win_currency'))
    max_win_nick_name = models.CharField(max_length=100, verbose_name=_('max_win_nick_name'))
    max_win_avatar_url = models.CharField(max_length=100, blank=True, verbose_name=_('max_win_avatar_url'))

    def __unicode__(self):
        return u'<{0}-{1}>'.format(self.cow_id, self.pool_currency)

    class Meta:
        db_table = 'fruit_pool'
        verbose_name = verbose_name_plural = ugettext('fruit_pool')

class AutoDeactiveLog(models.Model):
    _database = settings.LOGGER_DB

    user_id = models.PositiveIntegerField()
    reason = models.CharField(max_length=50, null=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('created_time'))

    class Meta:
        db_table = 'auto_deactive_log'
        verbose_name = verbose_name_plural = ugettext('auto_deactive_log')

    def __unicode__(self):
        return u'<{0}>'.format(self.user_id)
class PlayerCharge(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    charge_times = models.CharField(max_length=50, null=True)
    charge_money = models.BigIntegerField(default=0, verbose_name=_('charge_money'))

    @staticmethod
    def get_player_charge(user_id):
        try:
            return PlayerCharge.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            raise PlayerError.PLAYER_NOT_EXISTS(user_id=user_id)
        except MultipleObjectsReturned:
            raise
        except Exception:
            raise

    class Meta:
        db_table = 'player_charge'
        verbose_name = verbose_name_plural = ugettext('player_charge')

    def __unicode__(self):
        return u'<{0}>'.format(self.user_id)