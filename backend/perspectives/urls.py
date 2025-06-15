from django.urls import path
from .views import (
    PerspectiveListCreate,
    PerspectiveItemsListCreate,
    ItemListCreate,
    ValueListCreate,
    ValueDetail
)

urlpatterns = [
    path(
        route="perspectives",
        view=PerspectiveListCreate.as_view(),
        name="perspective_list"
    ),
    path(
        route="perspectives/create",
        view=PerspectiveListCreate.as_view(),
        name="perspective_create"
    ),
    path(
        route="perspectives/items",
        view=ItemListCreate.as_view(),
        name="perspective_all_items_list"
    ),
    path(
        route="perspectives/<int:perspective_id>/items",
        view=PerspectiveItemsListCreate.as_view(),
        name="perspective_items_list"
    ),
]
