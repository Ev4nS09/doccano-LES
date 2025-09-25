from django.urls import include, path

from .views import Me, UpdateEmail, UpdateFirstName, UpdateLastName, UpdatePassword, UpdateUsername, UserCreation, Users

urlpatterns = [
    path(route="me", view=Me.as_view(), name="me"),
    path(route="users", view=Users.as_view(), name="user_list"),
    path(route="users/create", view=UserCreation.as_view(), name="user_create"),
    path("auth/", include("dj_rest_auth.urls")),
	path("me/update-username/", UpdateUsername.as_view(), name="update-username"),
	path("me/update-password/", UpdatePassword.as_view(), name="update-password"),
    path("me/update-email/", UpdateEmail.as_view(), name="update-email"),  # Nova rota para atualizar o email
    path("me/update-first-name/", UpdateFirstName.as_view(), name="update-first-name"),
    path("me/update-last-name/", UpdateLastName.as_view(), name="update-last-name"),
]
