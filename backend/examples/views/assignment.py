from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from pydantic import ValidationError
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from labels.models import Category
from examples.assignment.strategies import StrategyName
from examples.assignment.usecase import bulk_assign
from examples.assignment.workload import WorkloadAllocation
from examples.models import Assignment
from examples.serializers import AssignmentSerializer, MemberWithLabelsSerializer
from projects.models import Member, Project
from projects.permissions import IsProjectAdmin, IsProjectMember, IsProjectStaffAndReadOnly


class AssignmentList(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    ordering_fields = ("created_at", "updated_at")
    model = Assignment

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs["project_id"])

    def get_queryset(self):
        queryset = self.model.objects.filter(project=self.project, assignee=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(project=self.project)


class AssignmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    lookup_url_kwarg = "assignment_id"
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsProjectStaffAndReadOnly)]


class ResetAssignment(APIView):
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    @property
    def project(self):
        return get_object_or_404(Project, pk=self.kwargs["project_id"])

    def delete(self, *args, **kwargs):
        Assignment.objects.filter(project=self.project).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BulkAssignment(APIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]

    def post(self, *args, **kwargs):
        try:
            strategy_name = StrategyName[self.request.data["strategy_name"]]
        except KeyError:
            return Response(
                {"detail": "Invalid strategy name"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            workload_allocation = WorkloadAllocation(workloads=self.request.data["workloads"])
        except ValidationError as e:
            return Response(
                {"detail": e.errors()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            bulk_assign(
                project_id=self.kwargs["project_id"],
                strategy_name=strategy_name,
                member_ids=workload_allocation.member_ids,
                weights=workload_allocation.weights,
            )
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_201_CREATED)

class ExampleMembersList(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]

    def get_queryset(self):
        example_id = self.kwargs["example_id"]
        project_id = self.kwargs["project_id"]

        # Verifica se o projeto existe
        project = get_object_or_404(Project, pk=project_id)

        # Filtra os assignments pelo example_id e project
        return Assignment.objects.filter(example_id=example_id, project=project)
    
class MemberWithLabelsView(APIView):
    permission_classes = [IsAuthenticated & IsProjectMember]

    def get(self, request, project_id, example_id):
        project = get_object_or_404(Project, pk=project_id)
        
        # Get all assignments for this example
        assignments = Assignment.objects.filter(
            example_id=example_id, 
            project=project
        ).select_related('assignee')
        
        # Get all categories for this example
        categories = Category.objects.filter(example_id=example_id)
        
        result = []
        for assignment in assignments:
            # Get the project member record
            member = Member.objects.filter(
                project=project,
                user=assignment.assignee
            ).first()
            
            member_labels = categories.filter(
                user=assignment.assignee
            ).values_list('label', flat=True)
            
            result.append({
                "member_id": member.id if member else None,  # Project member ID
                "assignee": assignment.assignee.id,
                "assignee_username": assignment.assignee.username,
                "labels": list(member_labels),
                "assignment_id": assignment.id  # Optional: include assignment ID if needed
            })
        
        serializer = MemberWithLabelsSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)