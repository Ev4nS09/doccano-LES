import json
import re
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import CategoryType, SpanType, RelationType, PerspectiveType

from .serializers import (
    PerspectiveSerializer,
    CategoryTypeSerializer,
    SpanTypeSerializer,
    RelationTypeSerializer,
)
from projects.models import Project
from projects.permissions import (
    IsProjectAdmin,
    IsProjectMember,
    IsProjectStaffAndReadOnly,
)

class PerspectiveList(generics.ListCreateAPIView):
    model = PerspectiveType
    filter_backends = [DjangoFilterBackend]
    serializer_class = PerspectiveSerializer
    pagination_class = None

    def get_permissions(self):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        if project.allow_member_to_create_label_type and self.request.method == "POST":
            self.permission_classes = [IsAuthenticated & IsProjectMember]
        else:
            self.permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]
        return super().get_permissions()

    def get_queryset(self):
        return self.model.objects.filter(project=self.kwargs["project_id"])

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs["project_id"])

    # não sei se está bem
    def delete(self, request, *args, **kwargs):
        ids = request.data.get("ids", [])
        self.model.objects.filter(id__in=ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PerspectiveDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsProjectAdmin | IsProjectMember]
    lookup_url_kwarg = "perspective_id"

class CategoryTypeList(PerspectiveList):
    model = CategoryType
    serializer_class = CategoryTypeSerializer

class SpanTypeList(PerspectiveList):
    model = SpanType
    serializer_class = SpanTypeSerializer

class RelationTypeList(PerspectiveList):
    model = RelationType
    serializer_class = RelationTypeSerializer

class CategoryTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoryType.objects.all()
    serializer_class = CategoryTypeSerializer
    lookup_url_kwarg = "perspective_id"
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]

class SpanTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpanType.objects.all()
    serializer_class = SpanTypeSerializer
    lookup_url_kwarg = "perspective_id"
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]

class RelationTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RelationType.objects.all()
    serializer_class = RelationTypeSerializer
    lookup_url_kwarg = "perspective_id"
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]
