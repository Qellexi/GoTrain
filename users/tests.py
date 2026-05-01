from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserRegistrationTest(APITestCase):
    def test_create_user(self):
        response = self.client.post(reverse("users:users-list"), {
            "email": "test@gotrain.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User",
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "test@gotrain.com")

    def test_create_user_no_password(self):
        response = self.client.post(reverse("users:users-list"), {
            "email": "test@gotrain.com",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_short_password(self):
        response = self.client.post(reverse("users:users-list"), {
            "email": "test@gotrain.com",
            "password": "123",
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserTokenTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gotrain.com",
            password="testpass123",
        )

    def test_obtain_token(self):
        response = self.client.post(reverse("users:token_obtain_pair"), {
            "email": "test@gotrain.com",
            "password": "testpass123",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_wrong_password(self):
        response = self.client.post(reverse("users:token_obtain_pair"), {
            "email": "test@gotrain.com",
            "password": "wrongpass",
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserMeTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gotrain.com",
            password="testpass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_get_me(self):
        response = self.client.get(reverse("users:users-me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@gotrain.com")

    def test_update_me(self):
        response = self.client.patch(reverse("users:users-me"), {
            "first_name": "Updated",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated")

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("users:users-me"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)