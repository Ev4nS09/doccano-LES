import uuid
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from examples.models import Example
from perspective_types.models import CategoryType, PerspectiveItem, SpanType, RelationType
from .managers import (
    PerspectiveManager,
    CategoryPerspectiveManager,
    SpanPerspectiveManager,
    TextPerspectiveManager,
    RelationPerspectiveManager,
    BoundingBoxPerspectiveManager,
    SegmentationPerspectiveManager,
)

class Perspective(models.Model):
    """
    Modelo abstrato base para as anotações de perspectives.
    """
    objects = PerspectiveManager()
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class CategoryPerspective(Perspective):
    """
    Anotação de perspective do tipo Categoria.
    """
    objects = CategoryPerspectiveManager()
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name="category")
    perspective = models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    item = models.ForeignKey(PerspectiveItem, on_delete=models.CASCADE, null=True, blank=False)

    class Meta:
        unique_together = ("example", "user", "perspective")
        app_label = 'perspectives'


class SpanPerspective(Perspective):
    """
    Anotação de perspective do tipo Span.
    """
    objects = SpanPerspectiveManager()
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name="span")
    perspective = models.ForeignKey(SpanType, on_delete=models.CASCADE)
    start_offset = models.IntegerField()
    end_offset = models.IntegerField()
    item = models.ForeignKey(PerspectiveItem, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        text = self.example.text[self.start_offset:self.end_offset]
        return f"({text}, {self.start_offset}, {self.end_offset}, {self.perspective.name})"

    def validate_unique(self, exclude=None):
        allow_overlapping = getattr(self.example.project, "allow_overlapping", False)
        is_collaborative = self.example.project.collaborative_annotation
        if allow_overlapping:
            super().validate_unique(exclude=exclude)
            return

        overlapping_span = (
            SpanPerspective.objects.exclude(id=self.id)
            .filter(example=self.example)
            .filter(
                models.Q(start_offset__gte=self.start_offset, start_offset__lt=self.end_offset)
                | models.Q(end_offset__gt=self.start_offset, end_offset__lte=self.end_offset)
                | models.Q(start_offset__lte=self.start_offset, end_offset__gte=self.end_offset)
            )
        )
        if is_collaborative:
            if overlapping_span.exists():
                raise ValidationError("Overlapping não é permitido neste projeto.")
        else:
            if overlapping_span.filter(user=self.user).exists():
                raise ValidationError("Overlapping não é permitido neste projeto.")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)

    def is_overlapping(self, other: "SpanPerspective"):
        return (
            (other.start_offset <= self.start_offset < other.end_offset)
            or (other.start_offset < self.end_offset <= other.end_offset)
            or (self.start_offset < other.start_offset and other.end_offset < self.end_offset)
        )

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(start_offset__gte=0), name="start_offset_gte_0"),
            models.CheckConstraint(check=models.Q(end_offset__gte=0), name="end_offset_gte_0"),
            models.CheckConstraint(check=models.Q(start_offset__lt=models.F("end_offset")), name="start_lt_end"),
        ]


class TextPerspective(Perspective):
    """
    Anotação de perspective baseada em texto.
    """
    objects = TextPerspectiveManager()
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name="text_perspectives")
    text = models.TextField()

    def is_same_text(self, other: "TextPerspective"):
        return self.text == other.text

    class Meta:
        unique_together = ("example", "user", "text")


class RelationPerspective(Perspective):
    """
    Anotação de perspective do tipo Relação.
    """
    objects = RelationPerspectiveManager()
    from_id = models.ForeignKey(SpanPerspective, on_delete=models.CASCADE, related_name="from_relations")
    to_id = models.ForeignKey(SpanPerspective, on_delete=models.CASCADE, related_name="to_relations")
    type = models.ForeignKey(RelationType, on_delete=models.CASCADE)
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name="relation")

    def __str__(self):
        text = self.example.text
        from_span = text[self.from_id.start_offset: self.from_id.end_offset]
        to_span = text[self.to_id.start_offset: self.to_id.end_offset]
        type_text = self.type.name
        return f"{from_span} - ({type_text}) -> {to_span}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)

    def clean(self):
        same_example = self.from_id.example == self.to_id.example == self.example
        if not same_example:
            raise ValidationError("Todas as relações devem referir o mesmo exemplo.")
        return super().clean()


class BoundingBoxPerspective(Perspective):
    """
    Anotação de perspective do tipo Bounding Box.
    """
    objects = BoundingBoxPerspectiveManager()
    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    perspective = models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    item = models.ForeignKey(PerspectiveItem, on_delete=models.CASCADE, null=True, blank=False)
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name="bbox")

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(x__gte=0), name="x_gte_0"),
            models.CheckConstraint(check=models.Q(y__gte=0), name="y_gte_0"),
            models.CheckConstraint(check=models.Q(width__gte=0), name="width_gte_0"),
            models.CheckConstraint(check=models.Q(height__gte=0), name="height_gte_0"),
        ]


class SegmentationPerspective(Perspective):
    """
    Anotação de perspective do tipo Segmentation.
    """
    objects = SegmentationPerspectiveManager()
    points = models.JSONField(default=list)
    perspective = models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    item = models.ForeignKey(PerspectiveItem, on_delete=models.CASCADE, null=True, blank=False)
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name="segmentation")
