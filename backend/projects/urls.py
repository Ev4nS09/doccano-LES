from django.urls import path

from .views.perspective import *
from .views.rule_discussion import VoteOnRule, RuleCommentListCreate, AnnotationRuleListCreate, AnnotationRuleDetail, RuleCommentDetail, RuleStatusUpdate
from .views.member import MemberDetail, MemberList, MyRole
from .views.project import CloneProject, ProjectDetail, ProjectList
from .views.tag import TagDetail, TagList

urlpatterns = [
    path(route="projects", view=ProjectList.as_view(), name="project_list"),
    path(route="projects/<int:project_id>", view=ProjectDetail.as_view(), name="project_detail"),
    path(route="projects/<int:project_id>/my-role", view=MyRole.as_view(), name="my_role"),
    path(route="projects/<int:project_id>/tags", view=TagList.as_view(), name="tag_list"),
    path(route="projects/<int:project_id>/tags/<int:tag_id>", view=TagDetail.as_view(), name="tag_detail"),
    path(route="projects/<int:project_id>/members", view=MemberList.as_view(), name="member_list"),
    path(route="projects/<int:project_id>/clone", view=CloneProject.as_view(), name="clone_project"),
    path(route="projects/<int:project_id>/members/<int:member_id>", view=MemberDetail.as_view(), name="member_detail"),
	path(route="projects/<int:project_id>/rules", view=AnnotationRuleListCreate.as_view(), name="rule_list"),
    path(route="projects/<int:project_id>/rules/<int:rule_id>", view=AnnotationRuleDetail.as_view(), name="rule_detail"),
    path(route="projects/<int:project_id>/rules/<int:rule_id>/vote", view=VoteOnRule.as_view(), name="rule_vote"),
    path(route="projects/<int:project_id>/rules/<int:rule_id>/comments", 
     view=RuleCommentListCreate.as_view(), 
     name="rule_comments"),
    path(route="projects/<int:project_id>/rules/<int:rule_id>/comments/<int:comment_id>", 
        view=RuleCommentDetail.as_view(), 
        name="rule_comment_detail"),
    path(
        route="projects/<int:project_id>/rules/<int:rule_id>/update-status",
        view=RuleStatusUpdate.as_view(),
        name='update-status'
    ),

    path('projects/<int:project_id>/perspectives', PerspectiveListCreateView.as_view(), name='perspective_list'),
    path('projects/<int:project_id>/perspectives/<int:perspective_id>', PerspectiveDeleteView.as_view(), name='perspective_delete'),

]
