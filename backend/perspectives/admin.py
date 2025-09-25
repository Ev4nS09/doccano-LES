from django.contrib import admin
from .models import Item, Value, Perspective
#from examples.models import Example

class PerspectiveAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']
    ordering = ['name']

class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_type', 'created_at']
    search_fields = ['name']
    ordering = ['name']

class ValueAdmin(admin.ModelAdmin):
    list_display = ['item', 'value', 'member', 'created_at']
    list_filter = ['member', 'item']
    search_fields = ['item__name']
    autocomplete_fields = ['member', 'item']  # Removed item_value from autocomplete
    ordering = ['-created_at']

    def get_value(self, obj):
        return obj.value

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Perspective, PerspectiveAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Value, ValueAdmin)
