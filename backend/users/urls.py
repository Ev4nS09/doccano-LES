from django.urls import include, path

from .views import Me, UserCreation, Users, UserDeletion

urlpatterns = [
    path(route="me", view=Me.as_view(), name="me"),
    path(route="users", view=Users.as_view(), name="user_list"),
    path(route="users/create", view=UserCreation.as_view(), name="user_create"),
    path("users/<int:pk>", UserDeletion.as_view(), name="user_delete"),
    path("auth/", include("dj_rest_auth.urls")),
]
