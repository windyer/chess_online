from rest_framework import serializers


class Fruit(serializers.Serializer):
    fruit_id = serializers.IntegerField()
    host = serializers.CharField()
    port = serializers.IntegerField()


class FruitServer(serializers.Serializer):
    fruit = Fruit(many=False, read_only=True)
    token = serializers.CharField(read_only=True)


class SelectFruitRequest(serializers.Serializer):
    fruit_id = serializers.IntegerField(min_value=1, max_value=4)