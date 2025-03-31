from rest_framework import serializers
from examples.models import Example
from perspective_types.models import PerspectiveItem
from .models import (
    CategoryPerspective,
    SpanPerspective,
    TextPerspective,
    RelationPerspective,
    BoundingBoxPerspective,
    SegmentationPerspective,
)
from perspective_types.models import CategoryType, SpanType, RelationType

class PerspectiveItemSerializer(serializers.ModelSerializer):
    """Serializador para os itens de uma perspetiva."""
    class Meta:
        model = PerspectiveItem
        fields = ['id', 'name']


class CategoryPerspectiveSerializer(serializers.ModelSerializer):
    """Serializador para as anotações de perspectiva do tipo Categoria."""
    example = serializers.PrimaryKeyRelatedField(queryset=Example.objects.all())
    perspective = serializers.PrimaryKeyRelatedField(queryset=CategoryType.objects.all())
    item = serializers.PrimaryKeyRelatedField(queryset=PerspectiveItem.objects.all())

    class Meta:
        model = CategoryPerspective
        fields = ['id', 'example', 'perspective', 'item', 'user']


class SpanPerspectiveSerializer(serializers.ModelSerializer):
    """Serializador para as anotações de perspectiva do tipo Span."""
    example = serializers.PrimaryKeyRelatedField(queryset=Example.objects.all())
    perspective = serializers.PrimaryKeyRelatedField(queryset=SpanType.objects.all())

    class Meta:
        model = SpanPerspective
        fields = ['id', 'example', 'perspective', 'start_offset', 'end_offset']


class TextPerspectiveSerializer(serializers.ModelSerializer):
    """Serializador para as anotações de perspectiva do tipo Texto."""
    example = serializers.PrimaryKeyRelatedField(queryset=Example.objects.all())

    class Meta:
        model = TextPerspective
        fields = ['id', 'example', 'text']


class RelationPerspectiveSerializer(serializers.ModelSerializer):
    """Serializador para as anotações de perspectiva do tipo Relação."""
    example = serializers.PrimaryKeyRelatedField(queryset=Example.objects.all())
    type = serializers.PrimaryKeyRelatedField(queryset=RelationType.objects.all())

    class Meta:
        model = RelationPerspective
        fields = ['id', 'example', 'from_id', 'to_id', 'type']


class BoundingBoxPerspectiveSerializer(serializers.ModelSerializer):
    """Serializador para as anotações de perspectiva do tipo Bounding Box."""
    example = serializers.PrimaryKeyRelatedField(queryset=Example.objects.all())
    perspective = serializers.PrimaryKeyRelatedField(queryset=CategoryType.objects.all())

    class Meta:
        model = BoundingBoxPerspective
        fields = ['id', 'example', 'perspective', 'x', 'y', 'width', 'height']


class SegmentationPerspectiveSerializer(serializers.ModelSerializer):
    """Serializador para as anotações de perspectiva do tipo Segmentação."""
    example = serializers.PrimaryKeyRelatedField(queryset=Example.objects.all())
    perspective = serializers.PrimaryKeyRelatedField(queryset=CategoryType.objects.all())

    class Meta:
        model = SegmentationPerspective
        fields = ['id', 'example', 'perspective', 'points']
