from card.lobby.service.view_service import ViewService

class FruitService(ViewService):

    def select_game(self, user_id, fruit_id):
        fruit_service = self.service_repositories.db.fruit_service
        return fruit_service.select_fruit(user_id, fruit_id)