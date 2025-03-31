from django.contrib import admin
from .models import CategoryType, SpanType, RelationType, PerspectiveType, PerspectiveItem

class PerspectiveItemInline(admin.TabularInline):
    model = PerspectiveItem
    extra = 1  # Número de linhas extras que aparecerão no formulário para adicionar novos itens
    fields = ('name',)  # Campos que você quer que apareçam para editar o item
    ordering = ('name',)

class PerspectiveTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "description", "created_at", "updated_at")
    ordering = ("project",)
    search_fields = ("name",)
    inlines = [PerspectiveItemInline]  # Adiciona os itens no formulário do tipo de perspetiva

class PerspectiveItemAdmin(admin.ModelAdmin):
    list_display = ("name", "perspective")
    ordering = ("perspective",)
    search_fields = ("name",)


class CategoryTypeAdmin(PerspectiveTypeAdmin):
    pass


class SpanTypeAdmin(PerspectiveTypeAdmin):
    pass


class RelationTypeAdmin(PerspectiveTypeAdmin):
    pass


admin.site.register(PerspectiveType, PerspectiveTypeAdmin)
admin.site.register(PerspectiveItem, PerspectiveItemAdmin)
admin.site.register(CategoryType, CategoryTypeAdmin)
admin.site.register(SpanType, SpanTypeAdmin)
admin.site.register(RelationType, RelationTypeAdmin)
