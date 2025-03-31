from django.urls import path
from .views import (
    CategoryTypeList,
    CategoryTypeDetail,
    SpanTypeList,
    SpanTypeDetail,
    RelationTypeList,
    RelationTypeDetail,
)

app_name = "perspective_types"

urlpatterns = [
    # Category Perspectives
    path("perspective-category-types", CategoryTypeList.as_view(), name="category_type_list"),
    path("perspective-category-types/<int:perspective_id>", CategoryTypeDetail.as_view(), name="category_type_detail"),
    
    # Span Perspectives
    path("perspective-span-types", SpanTypeList.as_view(), name="span_type_list"),
    path("perspective-span-types/<int:perspective_id>", SpanTypeDetail.as_view(), name="span_type_detail"),
    
    # Relation Perspectives
    path("perspective-relation-types", RelationTypeList.as_view(), name="relation_type_list"),
    path("perspective-relation-types/<int:perspective_id>", RelationTypeDetail.as_view(), name="relation_type_detail"),
]