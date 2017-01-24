from go import model
from go import containers

class DianyouUid(model.Model):
    uid = model.IntegerField()
    user_id = model.IntegerField()

    class Meta:
        db = containers.get_client()
        auto_increment = False

class DianyouUserId(model.Model):
    uid = model.IntegerField()
    user_id = model.IntegerField()

    class Meta:
        db = containers.get_client()
        auto_increment = False
