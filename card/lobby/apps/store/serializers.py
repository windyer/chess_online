from rest_framework import serializers

class PropertyItem(serializers.Serializer):
    item_id = serializers.IntegerField(read_only=True)
    count   = serializers.IntegerField(read_only=True)

class PurchaseItem(serializers.Serializer):
    item_id = serializers.IntegerField(min_value=1)
    count   = serializers.IntegerField(min_value=1)

class SellItem(serializers.Serializer):
    item_id = serializers.IntegerField(min_value=1)
    count   = serializers.IntegerField(min_value=1)

class PurchaseResponse(serializers.Serializer):
    item_id = serializers.IntegerField()
    currency = serializers.IntegerField()
    #cost = serializers.IntegerField()
    property_items = PropertyItem(many=True, source='items')


class SellResponse(serializers.Serializer):
    item_id = serializers.IntegerField()
    currency = serializers.IntegerField()
    #gain = serializers.IntegerField()
    property_items = PropertyItem(many=True, source='items')

class BullUrl(serializers.Serializer):
    url = serializers.CharField()

class StoreItem(serializers.Serializer):
    item_id = serializers.IntegerField(min_value=1)
    cat_food   = serializers.IntegerField(min_value=1)