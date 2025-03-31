from django.db import models
from projects.models import Project

class PerspectiveType(models.Model):
    """Representa uma perspetiva (grupo de itens relacionados)."""
    name = models.CharField(max_length=100, db_index=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('project', 'name')  # Nome único por projeto

    def __str__(self):
        return self.name


class PerspectiveItem(models.Model):
    """Representa um item individual de uma perspetiva (ex.: Masculino, Feminino, etc.)."""
    perspective = models.ForeignKey(PerspectiveType, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('perspective', 'name')  # Nome único por perspetiva

    def __str__(self):
        return self.name

class CategoryType(PerspectiveType):
    @property
    def perspectives(self):
        return CategoryType.objects.filter(project=self.project)


class SpanType(PerspectiveType):
    @property
    def perspectives(self):
        return SpanType.objects.filter(project=self.project)


class RelationType(PerspectiveType):
    @property
    def perspectives(self):
        return RelationType.objects.filter(project=self.project)