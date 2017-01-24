from rest_framework import serializers

class UpdateRequest(serializers.Serializer):
    platform = serializers.CharField(max_length=50, required=True)
    version = serializers.CharField(max_length=20, required=True)
    channel = serializers.CharField(max_length=50, required=True)