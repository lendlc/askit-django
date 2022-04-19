from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from api.models import User


# to run tests execute: python manage.py test <appname> -v 2
class AuthTest(APITestCase):
    # this func will run for every test
    def setUp(self):
        self.client = APIClient()
        
        #routes
        self.route_register='/api/v1/auth/register/'
        self.route_login='/api/v1/auth/login/'
        
        user = User(username = "test_user",email = "test_user@gmail.com")
        user.first_name = 'peter'
        user.last_name = 'griffin'
        user.role = 'tutor'
        user_pw = 'qwqw1212'
        user.set_password(user_pw)
        user.save()
        
        self.user = user
        
        self.credentials = {
            "username": self.user.email,
            "password": user_pw
        }
        
        self.invalid_credentails = {
            "username": "champy@gmail.com",
            "password": "champyisbestboi"
        }
    
        
    def test_user_was_created(self):
        count = User.objects.all().count()
        queryset = User.objects.get(email=self.user.email)
        self.assertNotEqual(count, 0)
        self.assertEqual(count, 1)
        self.assertEqual(queryset.email, self.user.email)
        
        
    def test_user_cannot_login_with_invalid_credentials(self):
        res = self.client.post(self.route_login, self.invalid_credentails, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
        
    def test_user_can_login(self):
        res = self.client.post(self.route_login, self.credentials, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    
    def test_login_has_valid_response(self):
        res = self.client.post(self.route_login, self.credentials, format='json')
        expected_keys = ['token', 'full_name', 'id', 'role']
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsInstance(res.data, dict)
        
        for k in expected_keys:
            self.assertIn(k, res.data.keys())
    
        
    def test_user_can_register(self):
        data = {
            "first_name": "kanye",
            "last_name": "west",
            "email": "kanye@gmail.com",
            "role": "tutor",
            "password": "qwqw1212"
        }
        res = self.client.post(self.route_register, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
    
    def test_user_cannot_register_with_duplicate_email(self):
        data = {
            "first_name": "kanye",
            "last_name": "west",
            "email": self.user.email,
            "role": "tutor",
            "password": "qwqw1212"
        }
        res = self.client.post(self.route_register, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', res.data.keys())
        
        
    def test_user_can_only_register_with_valid_role(self):
        data = {
            "first_name": "kanye",
            "last_name": "west",
            "email": "test_user1@gmail.com",
            "role": "role_model",
            "password": "qwqw1212"
        }
        res = self.client.post(self.route_register, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('role', res.data.keys())
