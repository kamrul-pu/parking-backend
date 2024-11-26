from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status

from common.base_test import BaseTest


User = get_user_model()


class UserTest(BaseTest):
    """Test all user-related APIs"""

    # def setUp(self):
    #     """Set up the test user and authentication"""
    #     super().setUp()

    #     # Create a superuser for authentication
    #     self.superuser_payload = {
    #         "first_name": "Super",
    #         "last_name": "Admin",
    #         "email": "superadmin@example.com",
    #         "password": "superadmin123",
    #     }
    #     User.objects.create_superuser(
    #         first_name=self.superuser_payload["first_name"],
    #         last_name=self.superuser_payload["last_name"],
    #         email=self.superuser_payload["email"],
    #         password=self.superuser_payload["password"],
    #     )

    #     # Login the superuser
    #     login_data = {
    #         "email": self.superuser_payload["email"],
    #         "password": self.superuser_payload["password"],
    #     }
    #     self.user_login = self.client.post(reverse("token_obtain_pair"), login_data)
    #     self.assertEqual(self.user_login.status_code, status.HTTP_200_OK)
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION="Bearer " + self.user_login.data["access"]
    #     )

    # Test User List API (GET and POST)
    def test_get_user_list(self):
        """Test GET request to fetch the list of users"""
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("id" in response.data["results"][0])
        self.assertTrue("email" in response.data["results"][0])

    def test_create_user(self):
        """Test POST request to create a new user"""
        new_user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "password": "password123",
            "confirm_password": "password123",
            "gender": "MALE",
        }
        response = self.client.post(reverse("user-list"), new_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], new_user_data["email"])

    # Test User Detail API (GET, PUT, DELETE)
    def test_get_user_detail(self):
        """Test GET request to retrieve a user’s details"""
        user = User.objects.create_user(
            first_name="Test",
            last_name="User",
            email="user@example.com",
            password="password123",
        )
        response = self.client.get(reverse("user-details", kwargs={"uid": user.uid}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], user.email)

    def test_update_user_detail(self):
        """Test PUT request to update a user’s details"""
        user = User.objects.create_user(
            first_name="Test",
            last_name="User",
            email="user@example.com",
            password="password123",
        )
        update_data = {
            "first_name": "Updated",
            "last_name": "User",
            "email": "updated@example.com",
            "gender": "FEMALE",
        }
        response = self.client.put(
            reverse("user-details", kwargs={"uid": user.uid}), update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], update_data["email"])

    def test_delete_user(self):
        """Test DELETE request to delete a user"""
        user = User.objects.create_user(
            first_name="Test",
            last_name="User",
            email="user@example.com",
            password="password123",
        )
        response = self.client.delete(reverse("user-details", kwargs={"uid": user.uid}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(uid=user.uid)

    # Test User Registration API (POST)
    def test_user_registration_success(self):
        """Test POST request to register a new user"""
        registration_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "password": "password123",
            "confirm_password": "password123",
            "gender": "MALE",
        }
        response = self.client.post(reverse("user-registration"), registration_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], registration_data["email"])

    def test_user_registration_password_mismatch(self):
        """Test POST request where password and confirm_password don't match"""
        registration_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "password": "password123",
            "confirm_password": "password124",  # Mismatch
            "gender": "Male",
        }
        response = self.client.post(reverse("user-registration"), registration_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Password and confirm password don't match", str(response.data))

    # Test Me Detail API (GET, PUT)
    def test_get_me_detail(self):
        """Test GET request to retrieve the current logged-in user's details"""
        response = self.client.get(reverse("me-detail"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.superuser_payload["email"])

    def test_update_me_detail(self):
        """Test PUT request to update the current logged-in user's details"""
        update_data = {
            "first_name": "Updated",
            "last_name": "Admin",
            "email": "updateduser@example.com",
            "gender": "MALE",
        }
        response = self.client.put(reverse("me-detail"), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], update_data["email"])
