from go import model
from go import containers

class YsdkUid(model.Model):
    open_id = model.CharField()
    user_id = model.IntegerField()
    account_type = model.CharField()
    class Meta:
        db = containers.get_client()
        auto_increment = False

class YsdkUserId(model.Model):
    open_id = model.CharField()
    user_id = model.IntegerField()
    account_type = model.CharField()


    class Meta:
        db = containers.get_client()
        auto_increment = False
