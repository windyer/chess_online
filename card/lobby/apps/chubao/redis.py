from go import model
from go import containers

class ChubaoUid(model.Model):
    uid = model.CharField()
    user_id = model.IntegerField()

    class Meta:
        db = containers.get_client()
        auto_increment = False

class ChubaoUserId(model.Model):
    uid = model.IntegerField()
    user_id = model.IntegerField()

    class Meta:
        db = containers.get_client()
        auto_increment = False
