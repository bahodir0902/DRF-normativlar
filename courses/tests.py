from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.utils import generate_random_username
from courses.models import Category

class CoursesAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@test.com', username=generate_random_username(), password='12')
        self.category = Category.objects.create(name="Test category")

    def get_jwt_token(self):
        return str(RefreshToken.for_user(self.user).access_token)

    def test_courses_crud(self):
        #GET
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #POST jwt bilan:
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_token()}")
        data = {
            "title": "Test",
            "description": "Test",
            "category": self.category.pk
        }
        response = self.client.post('/courses/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #PUT
        course_id = response.data['id']
        response = self.client.put(f"/courses/{course_id}/", {"title": "Updated title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Delete
        response = self.client.delete(f"/courses/{course_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_validation_error(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_token()}")
        response = self.client.post("/courses/", {}) # -> bo'sh POST method, xatolik berishi kerak
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
