from django.urls import path
from .views import (
    CategoryPerspectiveListAPI,
    CategoryPerspectiveDetailAPI,
    SpanPerspectiveListAPI,
    SpanPerspectiveDetailAPI,
    RelationPerspectiveListAPI,
    RelationPerspectiveDetailAPI,
)

app_name = "perspectives"

urlpatterns = [
    # Category Perspectives
    path(
        "examples/<int:example_id>/p-categories",
        CategoryPerspectiveListAPI.as_view(),
        name="category_perspective_list"
    ),
    path(
        "examples/<int:example_id>/p-categories/<int:annotation_id>",
        CategoryPerspectiveDetailAPI.as_view(),
        name="category_perspective_detail"
    ),

    # Span Perspectives
    path(
        "examples/<int:example_id>/p-spans",
        SpanPerspectiveListAPI.as_view(),
        name="span_perspective_list"
    ),
    path(
        "examples/<int:example_id>/p-spans/<int:annotation_id>",
        SpanPerspectiveDetailAPI.as_view(),
        name="span_perspective_detail"
    ),

    # Relation Perspectives
    path(
        "examples/<int:example_id>/p-relations",
        RelationPerspectiveListAPI.as_view(),
        name="relation_perspective_list"
    ),
    path(
        "examples/<int:example_id>/p-relations/<int:annotation_id>",
        RelationPerspectiveDetailAPI.as_view(),
        name="relation_perspective_detail"
    ),
]