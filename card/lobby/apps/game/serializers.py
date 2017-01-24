from rest_framework import serializers


class Game(serializers.Serializer):
    game_id = serializers.IntegerField()
    host = serializers.CharField()
    port = serializers.IntegerField()


class GameServer(serializers.Serializer):
    game = Game(many=False, read_only=True)
    token = serializers.CharField(read_only=True)


class SelectGameRequest(serializers.Serializer):
    mode = serializers.IntegerField(min_value=1, max_value=4)
    level = serializers.IntegerField(min_value=1, max_value=3)

        
class FollowGameRequest(serializers.Serializer):
    target_user_id = serializers.IntegerField(min_value=1)