from rest_framework import serializers
from .models import Item, Perspective, Value
from examples.models import Example

class PerspectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perspective 
        fields = [
            'id',
            'name',
            'items',
            'created_at',
            'updated_at'
        ]


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id',
            'name',
            'selection_list',
            'item_type',
            'created_at',
            'updated_at'
        ]

    def validate_item_type(self, value):
        allowed_types = ["int", "bool", "string", "float", "list"]
        if value not in allowed_types:
            raise serializers.ValidationError(f"Invalid item_type. Allowed values are: {allowed_types}")
        return value

class ValueSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    user_name = serializers.CharField(source='member.user.username', read_only=True)

    class Meta:
        model = Value
        fields = ['id', 'member', 'item', 'item_name', 'perspective', 'perspective_name', 'value', 'user_name', 'created_at']
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def validate(self, data):
        if data['value'].item != data['item']:
            raise serializers.ValidationError("Selected value doesn't belong to the specified item")
        return data
