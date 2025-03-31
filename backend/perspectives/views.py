from functools import partial
from typing import Type
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    CategoryPerspectiveSerializer,
    SpanPerspectiveSerializer,
    RelationPerspectiveSerializer,
    TextPerspectiveSerializer,
    BoundingBoxPerspectiveSerializer,
    SegmentationPerspectiveSerializer
)
from .models import (
    Perspective,
    CategoryPerspective,
    SpanPerspective,
    RelationPerspective,
    TextPerspective,
    BoundingBoxPerspective,
    SegmentationPerspective
)
from projects.models import Project
from projects.permissions import IsProjectMember


class BasePerspectiveListAPI(generics.ListCreateAPIView):
    perspective_class: Type[Perspective]  # Base type hint
    pagination_class = None
    permission_classes = [IsAuthenticated & IsProjectMember]
    swagger_schema = None

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs["project_id"])

    def get_queryset(self):
        queryset = self.perspective_class.objects.filter(example_id=self.kwargs["example_id"])
        if not self.project.collaborative_annotation:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        request.data["example"] = self.kwargs["example_id"]
        try:
            response = super().create(request, args, kwargs)
        except ValidationError as err:
            response = Response({"detail": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        return response

    def perform_create(self, serializer):
        serializer.save(example_id=self.kwargs["example_id"], user=self.request.user)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BasePerspectiveDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "annotation_id"
    swagger_schema = None

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs["project_id"])

    def get_permissions(self):
        if self.project.collaborative_annotation:
            self.permission_classes = [IsAuthenticated & IsProjectMember]
        else:
            self.permission_classes = [
                IsAuthenticated & IsProjectMember
            ]
        return super().get_permissions()


# Category Perspectives
class CategoryPerspectiveListAPI(BasePerspectiveListAPI):
    perspective_class = CategoryPerspective
    serializer_class = CategoryPerspectiveSerializer


class CategoryPerspectiveDetailAPI(BasePerspectiveDetailAPI):
    queryset = CategoryPerspective.objects.all()
    serializer_class = CategoryPerspectiveSerializer


# Span Perspectives
class SpanPerspectiveListAPI(BasePerspectiveListAPI):
    perspective_class = SpanPerspective
    serializer_class = SpanPerspectiveSerializer


class SpanPerspectiveDetailAPI(BasePerspectiveDetailAPI):
    queryset = SpanPerspective.objects.all()
    serializer_class = SpanPerspectiveSerializer


# Text Perspectives
class TextPerspectiveListAPI(BasePerspectiveListAPI):
    perspective_class = TextPerspective
    serializer_class = TextPerspectiveSerializer


class TextPerspectiveDetailAPI(BasePerspectiveDetailAPI):
    queryset = TextPerspective.objects.all()
    serializer_class = TextPerspectiveSerializer


# Relation Perspectives
class RelationPerspectiveListAPI(BasePerspectiveListAPI):
    perspective_class = RelationPerspective
    serializer_class = RelationPerspectiveSerializer


class RelationPerspectiveDetailAPI(BasePerspectiveDetailAPI):
    queryset = RelationPerspective.objects.all()
    serializer_class = RelationPerspectiveSerializer


# Bounding Box Perspectives
class BoundingBoxPerspectiveListAPI(BasePerspectiveListAPI):
    perspective_class = BoundingBoxPerspective
    serializer_class = BoundingBoxPerspectiveSerializer


class BoundingBoxPerspectiveDetailAPI(BasePerspectiveDetailAPI):
    queryset = BoundingBoxPerspective.objects.all()
    serializer_class = BoundingBoxPerspectiveSerializer


# Segmentation Perspectives
class SegmentationPerspectiveListAPI(BasePerspectiveListAPI):
    perspective_class = SegmentationPerspective
    serializer_class = SegmentationPerspectiveSerializer


class SegmentationPerspectiveDetailAPI(BasePerspectiveDetailAPI):
    queryset = SegmentationPerspective.objects.all()
    serializer_class = SegmentationPerspectiveSerializer