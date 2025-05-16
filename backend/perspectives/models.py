from django.db import models
from django.core.exceptions import ValidationError
from projects.models import Project, Member
from examples.models import Example
from django.contrib.auth.models import User

class Item(models.Model):
    """Classification item directly tied to a project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='classification_items')
    name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=100, default="list")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('project', 'name')
        ordering = ['name']

    def clean(self):
        allowed_types = ["int", "bool", "string", "float", "list"]
        if self.item_type not in allowed_types:
            raise ValidationError(f"Invalid p_type. Allowed values are: {allowed_types}")

    def __str__(self):
        return f"{self.name} ({self.project.name})"

class ItemValue(models.Model):
    """Predefined values for an item"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='predefined_values')
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('item', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.item.name}: {self.name}"

class Value(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    item_value = models.ForeignKey(ItemValue, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('member', 'item')
        ordering = ['-created_at']

    def __str__(self):
        if self.item_value:
            return f"{self.item.name}: {self.item_value.name} (by {self.member.user.username})"
        else:
            return self.value

    def clean(self):
        if self.member.role.name != "annotator":
            raise ValidationError("The value must be created by an annotator")

        if self.item_value:
            if self.item_value.item != self.item:
                raise ValidationError("Selected value doesn't belong to the specified item")


        expected_type = self.item.item_type
        val = self.value.strip()


          # Enforce item_value vs value nullability rules
        if expected_type == "list":
            if self.value:
                raise ValidationError("Value must be null when item_type is 'list'")
            if not self.item_value:
                raise ValidationError("item_value must be set when item_type is 'list'")
        else:
            if not self.value:
                raise ValidationError("Value must be set when item_type is not 'list'")
            if self.item_value:
                raise ValidationError("item_value must be null when item_type is not 'list'")

        try:
            if expected_type == "int":
                int(val)
            elif expected_type == "float":
                float(val)
            elif expected_type == "bool":
                if val.lower() not in ["true", "false"]:
                    raise ValueError("Not a boolean string")
            elif expected_type == "string":
                # Already a string, nothing to check
                pass
            elif expected_type == "list":
                pass
            else:
                raise ValidationError(f"Unknown p_type: {expected_type}")
        except Exception as e:
            raise ValidationError(f"Invalid value for type '{expected_type}': {e}")           
