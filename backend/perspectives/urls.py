from django.urls import path
from .views import (
    ItemListCreate,
    ValueListCreate,
    ValueDetail
)

urlpatterns = [
    path(
        route="projects/<int:project_id>/perspectives",
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
]
