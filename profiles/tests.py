from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profiles.models import Profile

User = get_user_model()


class ProfileAutoCreateTest(APITestCase):
    def test_profile_created_on_registration(self):
        self.client.post(reverse("users:users-list"), {
            "email": "test@gotrain.com",
            "password": "testpass123",
        })
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().user.email, "test@gotrain.com")


class ProfileMeTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@gotrain.com",
            password="testpass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_get_me(self):
        response = self.client.get(reverse("profiles:profiles-me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_phone_number(self):
        response = self.client.patch(reverse("profiles:profiles-me"), {
            "phone_number": "+380991112233",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], "+380991112233")

    def test_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("profiles:profiles-me"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
