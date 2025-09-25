from django.contrib import admin

from .models import (
    AnnotationRule,
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
    Ticket,
    TicketComment,
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


class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 0
    fields = ('author', 'content', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


class AnnotationRuleInline(admin.TabularInline):
    model = Ticket.rules.through
    extra = 1
    verbose_name = "Associated Rule"
    verbose_name_plural = "Associated Rules"


class AnnotationRuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'created_by', 'created_at', 'score')
    list_filter = ('project', 'created_by')
    search_fields = ('title', 'description')
    readonly_fields = ('score',)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'created_by', 'created_at', 'rule_count')
    list_filter = ('project', 'status', 'created_by')
    search_fields = ('title', 'description')
    inlines = [TicketCommentInline, AnnotationRuleInline]
    fieldsets = (
        (None, {
            'fields': ('project', 'title', 'description', 'status')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def rule_count(self, obj):
        return obj.rules.count()
    rule_count.short_description = 'Rules Count'


class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'author', 'created_at', 'content_preview')
    list_filter = ('ticket__project', 'author')
    search_fields = ('content',)
    readonly_fields = ('created_at', 'updated_at')

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


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
admin.site.register(AnnotationRule, AnnotationRuleAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketComment, TicketCommentAdmin)