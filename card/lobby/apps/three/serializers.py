from rest_framework import serializers


class Three(serializers.Serializer):
    three_id = serializers.IntegerField()
    host = serializers.CharField()
    port = serializers.IntegerField()


class ThreeServer(serializers.Serializer):
    three = Three(many=False, read_only=True)
    token = serializers.CharField(read_only=True)


class SelectThreeRequest(serializers.Serializer):
    three_id = serializers.IntegerField(min_value=1, max_value=4)