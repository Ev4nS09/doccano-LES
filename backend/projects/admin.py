from django.contrib import admin

from .models import (
    BoundingBoxProject,
    ImageCaptioningProject,
    ImageClassificationProject,
    Member,
    Project,
    SegmentationProject,
    Seq2seqProject,
    SequenceLabelingProject,
    Tag,
    TextClassificationProject,
    RuleComment,
    AnnotationRule,
    Perspective,
    UserPerspective,
)


class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "project",
    )
    ordering = ("user",)
    search_fields = ("user__username",)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "project_type", "random_order", "collaborative_annotation")
    ordering = ("project_type",)
    search_fields = ("name",)


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "text",
    )
    ordering = (
        "project",
        "text",
    )
    search_fields = ("text",)

class RuleCommentInline(admin.TabularInline):
    model = RuleComment
    extra = 0

class AnnotationRuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'created_by', 'created_at', 'score')
    list_filter = ('project', 'created_by')
    search_fields = ('title', 'description')
    inlines = [RuleCommentInline]

class PerspectiveAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'p_type', 'created_at', 'updated_at')
    list_filter = ('project', 'p_type', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

class UserPerspectiveAdmin(admin.ModelAdmin):
    list_display = ('perspective_name', 'user', 'perspective', 'value', 'created_at', 'updated_at')
    list_filter = ('perspective', 'user', 'created_at')
    search_fields = ('user__username', 'perpective__name', 'value')
    ordering = ('-created_at',)


admin.site.register(Member, MemberAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(TextClassificationProject, ProjectAdmin)
admin.site.register(SequenceLabelingProject, ProjectAdmin)
admin.site.register(Seq2seqProject, ProjectAdmin)
admin.site.register(BoundingBoxProject, ProjectAdmin)
admin.site.register(SegmentationProject, ProjectAdmin)
admin.site.register(ImageCaptioningProject, ProjectAdmin)
admin.site.register(ImageClassificationProject, ProjectAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(AnnotationRule,AnnotationRuleAdmin)
admin.site.register(Perspective,PerspectiveAdmin)
admin.site.register(UserPerspective,UserPerspectiveAdmin)
