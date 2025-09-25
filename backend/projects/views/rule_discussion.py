from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from perspectives.views import LargePagination
from projects.models import AnnotationRule, Ticket, TicketComment
from projects.permissions import IsProjectMember
from projects.serializers import AnnotationRuleSerializer, TicketCommentSerializer, TicketSerializer

class AnnotationRuleListCreate(generics.ListCreateAPIView):
    serializer_class = AnnotationRuleSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]

    def get_queryset(self):
        return AnnotationRule.objects.filter(project_id=self.kwargs['project_id'])

    def perform_create(self, serializer):
        serializer.save(project_id=self.kwargs['project_id'], created_by=self.request.user)

class AnnotationRuleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnnotationRule.objects.all()
    serializer_class = AnnotationRuleSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]
    lookup_url_kwarg = 'rule_id'

class VoteOnRule(APIView):
    permission_classes = [IsAuthenticated & IsProjectMember]

    def post(self, request, project_id, rule_id):
        rule = generics.get_object_or_404(AnnotationRule, pk=rule_id, project_id=project_id)
        vote = request.data.get('vote')  # 1 for upvote, -1 for downvote, 0 to remove vote

        if vote == 1:
            rule.upvotes.add(request.user)
            rule.downvotes.remove(request.user)
        elif vote == -1:
            rule.downvotes.add(request.user)
            rule.upvotes.remove(request.user)
        elif vote == 0:
            rule.upvotes.remove(request.user)
            rule.downvotes.remove(request.user)
        else:
            return Response({'error': 'Invalid vote value'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AnnotationRuleSerializer(rule, context={'request': request})
        return Response(serializer.data)

class TicketListCreate(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]

    def get_queryset(self):
        return Ticket.objects.filter(
            project_id=self.kwargs['project_id']
        ).select_related('created_by').prefetch_related('rules')

    def perform_create(self, serializer):
        serializer.save(
            project_id=self.kwargs['project_id'],
            created_by=self.request.user  # This will set both created_by and allow username lookup
        )

class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]
    lookup_url_kwarg = 'ticket_id'

    def get_queryset(self):
        return Ticket.objects.filter(project_id=self.kwargs['project_id'])

class TicketRulesUpdate(APIView):
    permission_classes = [IsAuthenticated & IsProjectMember]

    def post(self, request, project_id, ticket_id):
        ticket = get_object_or_404(Ticket, pk=ticket_id, project_id=project_id)
        rule_ids = request.data.get('rule_ids', [])
        
        # Validate rules belong to project
        rules = AnnotationRule.objects.filter(
            id__in=rule_ids,
            project_id=project_id
        )
        
        ticket.rules.add(*rules)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, project_id, ticket_id):
        ticket = get_object_or_404(Ticket, pk=ticket_id, project_id=project_id)
        rule_ids = request.data.get('rule_ids', [])
        ticket.rules.remove(*rule_ids)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TicketCommentListCreate(generics.ListCreateAPIView):
    serializer_class = TicketCommentSerializer
    permission_classes = [IsAuthenticated & IsProjectMember]

    def get_queryset(self):
        return TicketComment.objects.filter(
            ticket_id=self.kwargs['ticket_id'],
            ticket__project_id=self.kwargs['project_id']
        ).order_by('created_at')

    def perform_create(self, serializer):
        ticket = generics.get_object_or_404(
            Ticket, 
            pk=self.kwargs['ticket_id'], 
            project_id=self.kwargs['project_id']
        )
        serializer.save(ticket=ticket, author=self.request.user)


class RuleStatusUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated & IsProjectMember]
    queryset = AnnotationRule.objects.all()
    serializer_class = AnnotationRuleSerializer
    pagination_class = LargePagination

    STATUS_MAP = {
        0: "On going",
        1: "Approved",
        -1: "Rejected"
    }

    def patch(self, request, project_id, rule_id):
        rule = generics.get_object_or_404(AnnotationRule, pk=rule_id, project_id=project_id)

        status_value = request.data.get('status_value')

        if status_value not in self.STATUS_MAP:
            return Response({'error': 'Invalid status value'}, status=status.HTTP_400_BAD_REQUEST)

        rule.status = self.STATUS_MAP[status_value]
        rule.save()

        return Response({'status': rule.status}, status=status.HTTP_200_OK)