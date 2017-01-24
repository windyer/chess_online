from card.lobby.service.view_service import ViewService

class ThreeService(ViewService):

    def select_game(self, user_id, three_id):
        three_service = self.service_repositories.db.three_service
        return three_service.select_three(user_id, three_id)