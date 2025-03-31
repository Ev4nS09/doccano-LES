from django.contrib import admin
from .models import (
    CategoryPerspective,
    SpanPerspective,
    TextPerspective,
    RelationPerspective,
    BoundingBoxPerspective,
    SegmentationPerspective,
)

class SpanPerspectiveAdmin(admin.ModelAdmin):
    list_display = ("example", "perspective", "start_offset", "user")
    ordering = ("example",)

class CategoryPerspectiveAdmin(admin.ModelAdmin):
    list_display = ("example", "perspective", "item", "user")
    ordering = ("example",)
    list_filter = ("perspective", "item")  # Filtro para as perspectivas e seus itens


class TextPerspectiveAdmin(admin.ModelAdmin):
    list_display = ("example", "text", "user")
    ordering = ("example",)

class RelationPerspectiveAdmin(admin.ModelAdmin):
    list_display = ("example", "type", "user")
    ordering = ("example",)

class BoundingBoxPerspectiveAdmin(admin.ModelAdmin):
    list_display = ("example", "perspective", "user", "x", "y", "width", "height")
    ordering = ("example",)

class SegmentationPerspectiveAdmin(admin.ModelAdmin):
    list_display = ("example", "perspective", "user", "points")
    ordering = ("example",)

admin.site.register(CategoryPerspective, CategoryPerspectiveAdmin)
admin.site.register(SpanPerspective, SpanPerspectiveAdmin)
admin.site.register(TextPerspective, TextPerspectiveAdmin)
admin.site.register(RelationPerspective, RelationPerspectiveAdmin)
admin.site.register(BoundingBoxPerspective, BoundingBoxPerspectiveAdmin)
admin.site.register(SegmentationPerspective, SegmentationPerspectiveAdmin)
