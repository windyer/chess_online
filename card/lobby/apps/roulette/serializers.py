from rest_framework import serializers

import card.lobby.apps.roulette.models as roulette_models

class Roulette(serializers.Serializer):
    pass

class RouletteRecord(serializers.ModelSerializer):
    class Meta:
        model  = roulette_models.RouletteRecord
        fields = ('item_id', 'item_count',)

class NextRouletteType(serializers.Serializer):
    next_roulette_type = serializers.IntegerField()