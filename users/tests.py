# users/tests.py
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

CustomUser = get_user_model()


class UserProfileViewSetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='testpassword', phone='123456789', city='Test City')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_user_profiles(self):
        response = self.client.get('/user-profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_profile(self):
        response = self.client.get(f'/user-profile/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_profile(self):
        response = self.client.post('/user-profile/', {'email': 'newuser@example.com', 'password': 'newpassword', 'phone': '987654321', 'city': 'New City'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user_profile(self):
        response = self.client.put(f'/user-profile/{self.user.id}/', {'phone': '987654321', 'city': 'New City'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_user_profile(self):
        response = self.client.patch(f'/user-profile/{self.user.id}/', {'city': 'New City'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user_profile(self):
        response = self.client.delete(f'/user-profile/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_register_user(self):
        response = self.client.post('/register/', {'email': 'newuser@example.com', 'password': 'newpassword', 'phone': '987654321', 'city': 'New City'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_obtain_token(self):
        response = self.client.post('/token/', {'email': 'test@example.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        refresh_token = self.client.post('/token/', {'email': 'test@example.com', 'password': 'testpassword'}).data['refresh']
        response = self.client.post('/token/refresh/', {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
