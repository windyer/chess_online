import datetime
import time

import go.containers
from go import model
from django.utils import timezone

from card.core.conf import settings

current_timezone = timezone.get_current_timezone()

class PlayerExtra(model.Model):
    player_type = model.IntegerField() 
    last_login_time = model.DateTimeField()
    continuous_login_days = model.IntegerField(default=0)
    vip_award_steps = model.CharField(max_length=100)
    app_version = model.CharField(max_length=20)
    package_type = model.CharField(max_length=20)
    os_version = model.CharField(max_length=50)
    os_platform = model.CharField(max_length=50)
    channel = model.CharField(max_length=50)
    login_ip = model.CharField(max_length=20)
    login_device_id = model.CharField(max_length=32)
    created_time = model.DateTimeField()
    last_identify_time = model.DateTimeField()
    created_device_id = model.CharField()
    token = model.CharField(max_length=100)
    monthly_payment = model.BooleanField(default=False)
    monthly_pay_time = model.IntegerField(default=0) 
    monthly_unsubscribe_time = model.IntegerField(default=0) 
    monthly_continuous = model.BooleanField(default=False)
    monthly_end_time = model.IntegerField(default=0)
    monthly_mature_end = model.BooleanField(default=False)
    vender = model.CharField(max_length=32)
    networking = model.CharField(max_length=32)
    resolution = model.CharField(max_length=32)
    imei_number = model.CharField(max_length=32)
    bank_password = model.CharField(max_length=32)

    @property
    def has_logined_today(self):
        if self.last_login_time is None:
            return False
        today = timezone.datetime.now()
        last_login_time = self.last_login_time.astimezone(current_timezone)
        return (last_login_time.year == today.year
                and last_login_time.month == today.month
                and last_login_time.day == today.day)

    @property
    def has_identified_today(self):
        if self.last_identify_time is None:
            return False
        today = timezone.datetime.now()
        last_identify_time = self.last_identify_time.astimezone(current_timezone)
        return (last_identify_time.year == today.year
                and last_identify_time.month == today.month
                and last_identify_time.day == today.day)

    @property
    def has_logined_this_month(self):
        if self.last_login_time is None:
            return False
        today = timezone.datetime.now()
        last_login_time = self.last_login_time.astimezone(current_timezone)
        return (last_login_time.year == today.year
                and last_login_time.month == today.month)

    @property
    def monthly_payment_this_month(self):
        if not self.monthly_payment:
            return False
        if not self.monthly_pay_time:
            return False

        today = timezone.datetime.now()
        payment_date = datetime.datetime.fromtimestamp(self.monthly_pay_time)
        return (payment_date.year == today.year
                and payment_date.month == today.month)

    @property
    def is_monthly_player(self):
        if not self.monthly_payment:
            return False

        if self.monthly_continuous == False:
            if not self.monthly_mature_end:
                if self.monthly_payment_end_time <= 0:
                    return False
            else:
                if not self.monthly_payment_this_month:
                    return False
            
        return True

    @property
    def monthly_payment_end_time(self):
        now = int(time.time())
        if self.monthly_end_time <= now:
            return 0
        else:
            return now - self.monthly_end_time

    @property
    def first_day_login(self):
        if self.created_time is None:
            return True
        today = timezone.datetime.now()
        created_time = self.created_time.astimezone(current_timezone)
        return (created_time.year == today.year
                and created_time.month == today.month
                and created_time.day == today.day)
        
    @property
    def user_id(self):
        return self.id

    @property
    def first_time_login(self):
        if not self.first_day_login:
            return False
        else:  
            if not self.has_logined_today:
                return True
            if self.created_time is None:
                return True
            if self.last_login_time - self.created_time < datetime.timedelta(seconds=3):
                return True

        return False

    @property
    def created_today(self):
        if self.created_time is None:
            return False
        today = timezone.datetime.now()
        created_time = self.created_time.astimezone(current_timezone)
        return (created_time.year == today.year
                and created_time.month == today.month
                and created_time.day == today.day)

    @property
    def created_days(self):
        if self.created_time is None:
            return False
        today = timezone.now()
        created_time = self.created_time.astimezone(current_timezone)
        delta = today - created_time
        return delta.days

    class Meta:
        db = go.containers.get_client()
        auto_increment = False


class PlayerAlbum(model.Model):
    albums = model.DictField(key_type=int ,value_type=str)
    pending = model.DictField(key_type=int, value_type=str)

    @property
    def user_id(self):
        return self.id

    class Meta:
        db = go.containers.redis.Redis(**settings.PERSIST_REDIS)
        auto_increment = False
