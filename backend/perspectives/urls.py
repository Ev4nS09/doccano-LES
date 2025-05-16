from django.urls import path
from .views import (
    ExamplePerspectiveStats,
    ItemListCreate,
    ValueListCreate,
    ValueDetail
)

urlpatterns = [
    path(
        route="items",
        view=ItemListCreate.as_view(),
        name="item_list"
    ),
    path(
        route="examples/<int:example_id>/values",
        view=ValueListCreate.as_view(),
        name="value_list"
    ),
    path(
        route="examples/<int:example_id>/values/<int:pk>",
        view=ValueDetail.as_view(),
        name="value_detail"
    ),
    path(
        route="examples/<int:example_id>/perspective-stats",
        view=ExamplePerspectiveStats.as_view(),
        name="example_perspective_stats"
    ),
]