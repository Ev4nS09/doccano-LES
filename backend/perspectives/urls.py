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
        route="perspectives/<int:perspective_id>/items",
        view=PerspectiveItemsListCreate.as_view(),
        name="perspective_items_list"
    ),
]
