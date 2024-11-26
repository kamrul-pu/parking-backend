from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status


User = get_user_model()


class BaseTest(APITestCase):
    """Create a base test class to use multiple places"""

    def setUp(self):
        # Set up a test client
        self.client = APIClient()

        # Define payload
        self.superuser_payload = {
            "first_name": "Super",
            "last_name": "Admin",
            "email": "superadmin@example.com",
            "password": "superadmin123",
        }

        # Create a superuser
        User.objects.create_superuser(
            first_name=self.superuser_payload["first_name"],
            last_name=self.superuser_payload["last_name"],
            email=self.superuser_payload["email"],
            password=self.superuser_payload["password"],
        )

        # Login user and assert status
        login_data = {
            "email": self.superuser_payload["email"],
            "password": self.superuser_payload["password"],
        }
        self.user_login = self.client.post(reverse("token_obtain_pair"), login_data)
        self.assertEqual(self.user_login.status_code, status.HTTP_200_OK)

        # Set token for user
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"],
        )
