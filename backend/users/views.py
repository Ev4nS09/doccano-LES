from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password

from .serializers import UserSerializer
from projects.permissions import IsProjectAdmin


class Me(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class Users(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("username",)


class UserCreation(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user

class UpdateUsername(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        new_username = request.data.get("username")

        if new_username:
            # Verifica se o nome de usuário já está em uso
            if User.objects.filter(username=new_username).exists():
                return Response(
                    {"error": "Este nome de usuário já está em uso."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.username = new_username
            user.save()
            return Response({"message": "Nome de usuário atualizado com sucesso!"})

        return Response({"error": "O nome de usuário é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

class UpdatePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get("oldPassword")
        new_password = request.data.get("newPassword")

        # Debugging output
        print(f"Old Password: {old_password}, New Password: {new_password}")

        if not old_password or not new_password:
            return Response({"error": "Both old and new passwords are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the old password is correct
        if not check_password(old_password, user.password):
            return Response({"error": "Incorrect old password."}, status=status.HTTP_400_BAD_REQUEST)

        # Update password
        user.set_password(new_password)
        user.save()

        # Debugging output to check if password was updated
        print(f"User's password set to: {user.password}")

        return Response({"message": "Password updated successfully!"}, status=status.HTTP_200_OK)

class UpdateEmail(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        new_email = request.data.get("email")

        if not new_email:
            return Response({"error": "O email é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se o email já está em uso
        if User.objects.filter(email=new_email).exclude(id=user.id).exists():
            return Response({"error": "Este email já está em uso."}, status=status.HTTP_400_BAD_REQUEST)

        user.email = new_email
        user.save()
        return Response({"message": "Email atualizado com sucesso!"}, status=status.HTTP_200_OK)

class UpdateFirstName(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        new_first_name = request.data.get("first_name")

        if new_first_name is not None:
            user.first_name = new_first_name
            user.save()
            return Response({"message": "First name updated successfully!"})
        
        return Response({"error": "First name is required."}, status=status.HTTP_400_BAD_REQUEST)

class UpdateLastName(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        new_last_name = request.data.get("last_name")

        if new_last_name is not None:
            user.last_name = new_last_name
            user.save()
            return Response({"message": "Last name updated successfully!"})
        
        return Response({"error": "Last name is required."}, status=status.HTTP_400_BAD_REQUEST)