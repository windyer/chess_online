from rest_framework import serializers

class LoginChatRequest(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)
    text = serializers.CharField(read_only=True)