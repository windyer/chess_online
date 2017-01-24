from go import model
from go import containers

class HolyTreeUserName(model.Model):
    user_id = model.IntegerField()
    user_name = model.CharField()
    password = model.CharField()

    class Meta:
        db = containers.get_client()
        auto_increment = False

class HolyTreeUserId(model.Model):
    user_name = model.CharField()
    user_id = model.IntegerField()
    password = model.CharField()

    class Meta:
        db = containers.get_client()
        auto_increment = False

class GuestDeviceId(model.Model):
    device_id = model.CharField()
    user_id = model.IntegerField()

    class Meta:
        db = containers.get_client()
        auto_increment = False

class GuestUserId(model.Model):
    device_id = model.CharField()
    user_id = model.IntegerField()

    class Meta:
        db = containers.get_client()
        auto_increment = False