from rest_framework import serializers

class SalvageResponse(serializers.Serializer):
    currency = serializers.IntegerField(read_only=True)
    salvage_count = serializers.IntegerField(read_only=True)
    next_salvage_time = serializers.IntegerField(read_only=True)

class SalvageStatus(serializers.Serializer):
    salvage_interval = serializers.IntegerField(read_only=True)
    max_salvage_count = serializers.IntegerField(read_only=True)
    salvage_currency = serializers.IntegerField(read_only=True)
    salvage_criteria = serializers.IntegerField(read_only=True)
    salvage_count = serializers.IntegerField(read_only=True)
    next_salvage_time = serializers.IntegerField(read_only=True)

class MoneyTreeResponse(serializers.Serializer):
    currency = serializers.IntegerField(read_only=True)
    award_currency = serializers.IntegerField(read_only=True)
    fetch_end_time = serializers.IntegerField(read_only=True)

class MoneyTreeStatus(serializers.Serializer):
    fetch_end_time = serializers.IntegerField(read_only=True)
    available_time = serializers.IntegerField(read_only=True)
    fetch_interval_time = serializers.IntegerField(read_only=True)

class IosYouMiRequest(serializers.Serializer):
    order = serializers.CharField(max_length=50)
    app = serializers.CharField(max_length=50)
    ad = serializers.CharField(max_length=50)
    adid = serializers.CharField()
    user = serializers.IntegerField()
    device = serializers.CharField()
    chn = serializers.IntegerField()
    price = serializers.FloatField()
    points = serializers.IntegerField()
    time = serializers.IntegerField()
    sig = serializers.CharField(max_length=50)
    sign = serializers.CharField(max_length=50)

class AndroidYouMiRequest(serializers.Serializer):
    order = serializers.CharField(max_length=50)
    app = serializers.CharField(max_length=50)
    ad = serializers.CharField(max_length=50)
    user = serializers.IntegerField()
    device = serializers.CharField()
    chn = serializers.IntegerField()
    points = serializers.IntegerField()
    time = serializers.IntegerField()
    sig = serializers.CharField(max_length=50)

class ScoreWallRequest(serializers.Serializer):
    order_id = serializers.CharField(max_length=100)
    score = serializers.IntegerField(min_value=1)
    sign = serializers.CharField(max_length=50)

class ScoreWallResponse(serializers.Serializer):
    award_currency = serializers.IntegerField()
    currency = serializers.IntegerField()