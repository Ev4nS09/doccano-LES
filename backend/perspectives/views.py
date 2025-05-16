from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.shortcuts import get_object_or_404
from examples.models import Example
from projects.models import Project
from projects.permissions import IsProjectMember
from .models import Item, Value
from .serializers import ItemSerializer, ValueSerializer

class ItemListCreate(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]
    
    def get_queryset(self):
        return Item.objects.filter(project_id=self.kwargs['project_id'])
    
    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        serializer.save(project=project)

class ValueListCreate(generics.ListCreateAPIView):
    serializer_class = ValueSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]
    
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

class ValueDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ValueSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]
