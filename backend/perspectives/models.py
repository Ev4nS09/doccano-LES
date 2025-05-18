from django.db import models
from django.core.exceptions import ValidationError
from projects.models import Project, Member
from examples.models import Example
from django.contrib.auth.models import User

class Item(models.Model):
    """Classification item directly tied to a project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='classification_items')
    name = models.CharField(max_length=100)
    selection_list = models.JSONField(blank=True, default=list)
    item_type = models.CharField(max_length=100)
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

class Value(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.TextField()

    class Meta:
        unique_together = ('member', 'item')
        ordering = ['-created_at']

    def __str__(self):
        return self.value

    def clean(self):
        if self.member.role.name != "annotator":
            raise ValidationError("The value must be created by an annotator")


        expected_type = self.item.item_type
        val = self.value.strip()

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
                if val not in self.item.selection_list:
                    raise ValidationError(f"Value must be one of: {self.item.selection_list}")
            else:
                raise ValidationError(f"Unknown p_type: {expected_type}")
        except Exception as e:
            raise ValidationError(f"Invalid value for type '{expected_type}': {e}")           
