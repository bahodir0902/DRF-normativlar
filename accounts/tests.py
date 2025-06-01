from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.utils import generate_random_username

class AccountsAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@test.com', username=generate_random_username(), password='12')

    def get_jwt_token(self):
        return str(RefreshToken.for_user(self.user).access_token)

    def test_register(self):
        data = {
            "email": "test@new.com",
            "username": generate_random_username(),
            "password": "12",
            "re_password": "12"
        }
        response = self.client.post('/accounts/register/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_jwt(self):
        data = {
            "email": "test@test.com",
            "password": "12"
        }
        response = self.client.post('/accounts/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
