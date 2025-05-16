from rest_framework import serializers
from .models import Item, ItemValue, Value
from examples.models import Example

class ItemValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemValue
        fields = ['id', 'name', 'created_at']

class ItemSerializer(serializers.ModelSerializer):
    predefined_values = ItemValueSerializer(many=True, read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'project', 'project_name', 'name', 'predefined_values', 'created_at', 'updated_at']

class ValueSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    value_name = serializers.CharField(source='item_value.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Value
        fields = ['id', 'user', 'item', 'item_name', 'item_value', 'value_name', 'user_name', 'created_at']
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def validate(self, data):
        if data['item_value'].item != data['item']:
            raise serializers.ValidationError("Selected value doesn't belong to the specified item")
        return data
