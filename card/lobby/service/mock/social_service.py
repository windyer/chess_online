__all__ = ['SocialService']

class SocialService(object):

    def request_friend(self, user_id, target_user_id, gift_id=None):
        pass

    def accept_friend(self, user_id, target_user_id):
        pass

    def decline_friend(self, user_id, target_user_id):
        pass

    def send_currency(self, user_id, target_user_id, delta_currency):
        pass
