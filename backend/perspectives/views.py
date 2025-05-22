from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.shortcuts import get_object_or_404
from examples.models import Example
#from projects.models import Project
from projects.permissions import IsProjectMember
from .models import Perspective, Item, Value
from .serializers import PerspectiveSerializer, ItemSerializer, ValueSerializer

class PerspectiveListCreate(generics.ListCreateAPIView):
    serializer_class = PerspectiveSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]
    queryset = Perspective.objects.all()

    
class PerspectiveItemsListCreate(generics.ListAPIView):
    """
    List all items belonging to a specific perspective
    """
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        perspective_id = self.kwargs['perspective_id']
        perspective = get_object_or_404(Perspective, id=perspective_id)
        return perspective.items.all()

class ItemListCreate(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]

class ValueListCreate(generics.ListCreateAPIView):
    serializer_class = ValueSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]
    
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

class ValueDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ValueSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]
