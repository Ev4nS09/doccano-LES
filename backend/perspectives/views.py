from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.db.models import Count
from django.shortcuts import get_object_or_404
from projects.models import Member
from examples.models import Example
#from projects.models import Project
from projects.permissions import IsProjectMember
from .models import Perspective, Item, Value
from .serializers import MemberFilterSerializer, PerspectiveSerializer, ItemSerializer, ValueSerializer

from rest_framework.pagination import PageNumberPagination

class LargePagination(PageNumberPagination):
    page_size = 100 

class PerspectiveListCreate(generics.ListCreateAPIView):
    serializer_class = PerspectiveSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]
    queryset = Perspective.objects.all()
    pagination_class = LargePagination

    
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

class ValueDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ValueSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]
    pagination_class = LargePagination


class FilterMembersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated & IsProjectMember]
    
    def get_queryset(self):
        project_id = self.kwargs['project_id']
        filters = self.request.query_params
        
        # Get all members in project initially
        members = Member.objects.filter(project_id=project_id)
        
        # Process each filter
        for param, value in filters.items():
            if param == 'project_id':  # Skip project_id as it's already used
                continue
                
            # Handle numeric range filters (min/max)
            if param.endswith('_min') or param.endswith('_max'):
                item_name = param.rsplit('_', 1)[0]
                comparison = 'gte' if param.endswith('_min') else 'lte'
                
                # Get values that match the numeric condition
                matching_values = Value.objects.filter(
                    item__name=item_name,
                    item__item_type__in=['int', 'float'],  # Only numeric types
                    member__project_id=project_id
                )
                
                # Convert to numeric comparison
                member_ids = []
                for val in matching_values:
                    try:
                        numeric_value = float(val.value)
                        filter_value = float(value)
                        if comparison == 'gte' and numeric_value >= filter_value:
                            member_ids.append(val.member_id)
                        elif comparison == 'lte' and numeric_value <= filter_value:
                            member_ids.append(val.member_id)
                    except (ValueError, TypeError):
                        continue
                
                members = members.filter(id__in=member_ids)
            
            else:
                # Handle exact match filters
                member_ids = Value.objects.filter(
                    item__name=param,
                    member__project_id=project_id,
                    value=value
                ).values_list('member_id', flat=True)
                
                members = members.filter(id__in=member_ids)
        
        return members.distinct()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response({
            'user_ids': list(queryset.values_list('user', flat=True)),
            'count': queryset.count()
        })