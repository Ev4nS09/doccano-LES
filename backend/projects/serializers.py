from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import (
    BoundingBoxProject,
    ImageCaptioningProject,
    ImageClassificationProject,
    IntentDetectionAndSlotFillingProject,
    Member,
    Project,
    SegmentationProject,
    Seq2seqProject,
    SequenceLabelingProject,
    Speech2textProject,
    Tag,
    TextClassificationProject,
    AnnotationRule,
    RuleComment,
    Perspective,
    UserPerspective,
)


class MemberSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    rolename = serializers.SerializerMethodField()

    @classmethod
    def get_username(cls, instance):
        user = instance.user
        return user.username if user else None

    @classmethod
    def get_rolename(cls, instance):
        role = instance.role
        return role.name if role else None

    class Meta:
        model = Member
        fields = ("id", "user", "role", "username", "rolename")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "project",
            "text",
        )
        read_only_fields = ("id", "project")


class ProjectSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    author = serializers.SerializerMethodField()

    @classmethod
    def get_author(cls, instance):
        if instance.created_by:
            return instance.created_by.username
        return ""

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "guideline",
            "project_type",
            "created_at",
            "updated_at",
            "random_order",
            "author",
            "collaborative_annotation",
            "single_class_classification",
            "allow_member_to_create_label_type",
            "is_text_project",
            "tags",
        ]
        read_only_fields = (
            "created_at",
            "updated_at",
            "author",
            "is_text_project",
        )

    def create(self, validated_data):
        tags = TagSerializer(data=validated_data.pop("tags", []), many=True)
        project = self.Meta.model.objects.create(**validated_data)
        tags.is_valid()
        tags.save(project=project)
        return project

    def update(self, instance, validated_data):
        # Don't update tags. Please use TagAPI.
        validated_data.pop("tags", None)
        return super().update(instance, validated_data)


class TextClassificationProjectSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        model = TextClassificationProject


class SequenceLabelingProjectSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        model = SequenceLabelingProject
        fields = ProjectSerializer.Meta.fields + ["allow_overlapping", "grapheme_mode", "use_relation"]


class Seq2seqProjectSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        model = Seq2seqProject


class IntentDetectionAndSlotFillingProjectSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        model = IntentDetectionAndSlotFillingProject


class Speech2textProjectSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        model = Speech2textProject


class ImageClassificationProjectSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        model = ImageClassificationProject


class BoundingBoxProjectSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        model = BoundingBoxProject


class SegmentationProjectSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        model = SegmentationProject


class ImageCaptioningProjectSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        model = ImageCaptioningProject


class ProjectPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Project: ProjectSerializer,
        **{cls.Meta.model: cls for cls in ProjectSerializer.__subclasses__()},
    }

class PerspectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perspective
        fields = ['id', 'name', 'project', 'selection_list', 'p_type', 'created_at', 'updated_at']

class UserPerspectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPerspective
        fields = ['id', 'perspective', 'user', 'value', 'created_at', 'updated_at']

class RuleCommentSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()

    def get_author_username(self, obj):
        return obj.author.username

    class Meta:
        model = RuleComment
        fields = ['id', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

class AnnotationRuleSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    author_username = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()

    def get_comments(self, obj):
        # Only include comments if specifically requested
        if self.context.get('include_comments', False):
            return RuleCommentSerializer(obj.comments.all(), many=True).data
        return []

    def get_author_username(self, obj):
        return obj.created_by.username if obj.created_by else None

    def get_score(self, obj):
        return obj.score

    def get_user_vote(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if obj.upvotes.filter(id=request.user.id).exists():
                return 1
            elif obj.downvotes.filter(id=request.user.id).exists():
                return -1
        return 0

    class Meta:
        model = AnnotationRule
        fields = ['id', 'project', 'title', 'description', 'created_by', 'author_username', 
                 'created_at', 'updated_at', 'score', 'user_vote', 'comments', 'upvotes', 'downvotes', 'status']
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'score', 'user_vote', 'upvotes', 'downvotes']
