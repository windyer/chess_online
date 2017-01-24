from rest_framework import serializers

class Post(serializers.Serializer):
    click_time = serializers.CharField()
    user_id = serializers.IntegerField()