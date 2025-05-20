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
]
