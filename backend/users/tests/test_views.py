from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from .utils import make_user


class TestUserAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = make_user(username="bob")
        cls.url = reverse(viewname="user_list")

    def test_allows_authenticated_user_to_get_users(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], self.user.username)

    def test_denies_unauthenticated_user_to_get_users(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestMeAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = make_user(username="bob")
        cls.url = reverse(viewname="me")

    def test_return_own_information(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.data["id"], self.user.id)
        self.assertEqual(response.data["username"], self.user.username)

    def test_does_not_return_information_to_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestUserCreationAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff = make_user(username="bob", is_staff=True)
        cls.non_staff = make_user(username="tom", is_staff=False)
        cls.url = reverse(viewname="user_create")
        cls.payload = {"username": "hironsan", "password1": "foobarbaz", "password2": "foobarbaz"}

    def test_staff_can_create_user(self):
        self.client.force_login(self.staff)
        response = self.client.post(self.url, data=self.payload)
        self.assertEqual(response.data["username"], "hironsan")

    def test_non_staff_cannot_create_user(self):
        self.client.force_login(self.non_staff)
        response = self.client.post(self.url, data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestUpdateUsernameAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = make_user(username="bob")
        cls.url = reverse("update-username")

    def test_authenticated_user_can_update_username(self):
        self.client.force_login(self.user)
        response = self.client.put(self.url, {"username": "new_bob"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "new_bob")

    def test_cannot_update_username_to_existing_one(self):
        existing_user = make_user(username="alice")
        self.client.force_login(self.user)
        response = self.client.put(self.url, {"username": "alice"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Este nome de usuário já está em uso.", response.data["error"])

    def test_cannot_update_username_when_unauthenticated(self):
        response = self.client.put(self.url, {"username": "new_bob"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestUpdatePasswordAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="bob", email="bob@example.com", password="old_password")
        cls.url = reverse("update-password")

    def test_authenticated_user_can_update_password(self):
        self.client.force_login(self.user)
        response = self.client.put(self.url, {"oldPassword": "old_password", "newPassword": "new_secure_password"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("new_secure_password"))

    def test_cannot_update_password_with_wrong_old_password(self):
        self.client.force_login(self.user)
        response = self.client.put(self.url, {"oldPassword": "wrong_password", "newPassword": "new_secure_password"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Incorrect old password.", response.data["error"])

    def test_cannot_update_password_when_unauthenticated(self):
        response = self.client.put(self.url, {"oldPassword": "old_password", "newPassword": "new_secure_password"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestUpdateEmailAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="bob", email="bob@example.com", password="old_password")
        cls.url = reverse("update-email")

    def test_authenticated_user_can_update_email(self):
        self.client.force_login(self.user)
        response = self.client.put(self.url, {"email": "new_email@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "new_email@example.com")

    def test_cannot_update_email_to_existing_one(self):
        existing_user = User.objects.create_user(username="alice", email="alice@example.com")
        self.client.force_login(self.user)
        response = self.client.put(self.url, {"email": "alice@example.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Este email já está em uso.", response.data["error"])

    def test_cannot_update_email_when_unauthenticated(self):
        response = self.client.put(self.url, {"email": "new_email@example.com"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)