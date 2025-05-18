from rest_framework import serializers
from .models import Item, Value
from examples.models import Example

class ItemSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Item
        fields = [
                  'id', 
                  'project', 
                  'project_name', 
                  'name', 
                  'item_type', 
                  'selection_list',
                  'predefined_values', 
                  'created_at', 
                  'updated_at'
                  ]

class ValueSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    user_name = serializers.CharField(source='member.user.username', read_only=True)

    class Meta:
        model = Value
        fields = ['id', 'member', 'item', 'item_name', 'value', 'user_name', 'created_at']
        extra_kwargs = {
            'user': {'write_only': True}
        }

    def validate(self, data):
        if data['value'].item != data['item']:
            raise serializers.ValidationError("Selected value doesn't belong to the specified item")
        return data
