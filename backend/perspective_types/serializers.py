from rest_framework import serializers
from .models import PerspectiveType, PerspectiveItem, CategoryType, SpanType, RelationType


class PerspectiveItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerspectiveItem
        fields = ['id', 'name', 'perspective']


class PerspectiveSerializer(serializers.ModelSerializer):
    items = PerspectiveItemSerializer(many=True, read_only=True)

    class Meta:
        model = PerspectiveType
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'items']


class CategoryTypeSerializer(PerspectiveSerializer):
    class Meta(PerspectiveSerializer.Meta):
        model = CategoryType
        fields = PerspectiveSerializer.Meta.fields


class SpanTypeSerializer(PerspectiveSerializer):
    class Meta(PerspectiveSerializer.Meta):
        model = SpanType
        fields = PerspectiveSerializer.Meta.fields


class RelationTypeSerializer(PerspectiveSerializer):
    class Meta(PerspectiveSerializer.Meta):
        model = RelationType
        fields = PerspectiveSerializer.Meta.fields
