from django.db.models import Count, Manager

class PerspectiveManager(Manager):
    """
    Manager base para as operações com perspectives.
    """
    perspective_type_field = "label"  # Campo de referência da perspective; usa "type" para relações se necessário

    def calc_perspective_distribution(self, examples, members, perspectives):
        """
        Calcula a distribuição dos itens de perspective por utilizador.
        Retorna um dicionário no formato:
        {username: {nome_da_perspective: count, ...}, ...}
        """
        distribution = {
            member.username: {persp.name: 0 for persp in perspectives}
            for member in members
        }
        items = (
            self.filter(example_id__in=examples)
            .values("user__username", f"{self.perspective_type_field}__name")
            .annotate(count=Count(f"{self.perspective_type_field}__name"))
        )
        for item in items:
            username = item["user__username"]
            perspective_name = item[f"{self.perspective_type_field}__name"]
            count = item["count"]
            distribution[username][perspective_name] = count
        return distribution

    def get_perspectives(self, perspective, project):
        """
        Retorna os itens de perspective associados ao mesmo exemplo,
        respeitando se a anotação é colaborativa ou individual.
        """
        if project.collaborative_annotation:
            return self.filter(example=perspective.example)
        else:
            return self.filter(example=perspective.example, user=perspective.user)

    def can_annotate(self, perspective, project) -> bool:
        raise NotImplementedError("Implemente este método na subclasse.")

    def filter_annotatable_perspectives(self, perspectives, project):
        return [p for p in perspectives if self.can_annotate(p, project)]


class CategoryPerspectiveManager(PerspectiveManager):
    def can_annotate(self, perspective, project) -> bool:
        is_exclusive = project.single_class_classification
        categories = self.get_perspectives(perspective, project)
        if is_exclusive:
            return not categories.exists()
        else:
            return not categories.filter(label=perspective.label).exists()


class SpanPerspectiveManager(PerspectiveManager):
    def can_annotate(self, perspective, project) -> bool:
        overlapping = getattr(project, "allow_overlapping", False)
        spans = self.get_perspectives(perspective, project)
        if overlapping:
            return True
        for span in spans:
            if span.is_overlapping(perspective):
                return False
        return True


class TextPerspectiveManager(PerspectiveManager):
    def can_annotate(self, perspective, project) -> bool:
        texts = self.get_perspectives(perspective, project)
        for text in texts:
            if text.is_same_text(perspective):
                return False
        return True


class RelationPerspectiveManager(PerspectiveManager):
    perspective_type_field = "type"  # Para relações, usamos o campo "type"

    def can_annotate(self, perspective, project) -> bool:
        return True


class BoundingBoxPerspectiveManager(PerspectiveManager):
    def can_annotate(self, perspective, project) -> bool:
        return True


class SegmentationPerspectiveManager(PerspectiveManager):
    def can_annotate(self, perspective, project) -> bool:
        return True
