from django.contrib import admin
from .models import Item, ItemValue, Value
from examples.models import Example

class ItemValueInline(admin.TabularInline):
    model = ItemValue
    extra = 1
    fields = ['name']
    ordering = ['name']

class ItemValueAdmin(admin.ModelAdmin):
    list_display = ['name', 'item', 'created_at']
    list_filter = ['item__project']
    search_fields = ['name', 'item__name']
    ordering = ['name']

class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemValueInline]
    list_display = ['name', 'project', 'created_at']
    list_filter = ['project']
    search_fields = ['name']
    ordering = ['name']

class ValueAdmin(admin.ModelAdmin):
    list_display = ['item', 'get_value', 'member', 'created_at']
    list_filter = ['item__project', 'member', 'item']
    search_fields = ['item_value__name', 'item__name']
    autocomplete_fields = ['member', 'item']  # Removed item_value from autocomplete
    ordering = ['-created_at']

    def get_value(self, obj):
        if obj.item_value:
            return obj.item_value.name
        else:
            return obj.value

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemValue, ItemValueAdmin)  # Added this line
admin.site.register(Value, ValueAdmin)
