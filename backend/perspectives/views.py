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

from rest_framework.pagination import PageNumberPagination

class LargePagination(PageNumberPagination):
    page_size = 100 

class PerspectiveListCreate(generics.ListCreateAPIView):
    serializer_class = PerspectiveSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]
    queryset = Perspective.objects.all()
    pagination_class = LargePagination


class PerspectiveDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Perspective.objects.all()
    serializer_class = PerspectiveSerializer
    lookup_url_kwarg = "perspective_id"
    
class PerspectiveItemsListCreate(generics.ListAPIView):
    """
    List all items belonging to a specific perspective
    """
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LargePagination

    def get_queryset(self):
        perspective_id = self.kwargs['perspective_id']
        perspective = get_object_or_404(Perspective, id=perspective_id)
        return perspective.items.all()

class ItemListCreate(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]
    queryset = Item.objects.all()
    pagination_class = LargePagination

class ValueListCreate(generics.ListCreateAPIView):
    serializer_class = ValueSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]
    pagination_class = LargePagination
    
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context

class ValueDetail(generics.ListAPIView):
    serializer_class = ValueSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]
    pagination_class = LargePagination

    def get_queryset(self):
        member_id = self.kwargs['member_id']
        return Value.objects.filter(member_id=member_id)
