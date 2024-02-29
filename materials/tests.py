# materials/tests.py
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from materials.models import Course

CustomUser = get_user_model()


class CourseCRUDTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='testpassword', phone='123456789', city='Test City')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        response = self.client.post('/courses/', {'title': 'Test Course', 'description': 'Test Description'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_course(self):
        course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        response = self.client.get(f'/courses/{course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_course(self):
        course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        response = self.client.patch(f'/courses/{course.id}/', {'title': 'Updated Title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_course(self):
        course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        response = self.client.delete(f'/courses/{course.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='testpassword', phone='123456789', city='Test City')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        response = self.client.post('/subscriptions/', {'course_id': course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_subscription(self):
        course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        self.client.post('/subscriptions/', {'course_id': course.id})
        response = self.client.delete(f'/subscriptions/{course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
