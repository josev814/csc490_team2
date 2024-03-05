import json
from django.test import RequestFactory, TestCase
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import ValidationError

from auth import views

# Create your tests here.
class AuthTestCases(TestCase):
    user_dict = {
        'email': 'ccjvsj@mailinator.com',
        'password': 'UnitTestingPassword'
    }
    user_id = 1

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_missing_email_create_user(self):
        user_dict = self.user_dict.copy()
        user_dict.pop('email')
        request = self.factory.post('/auth/register', user_dict)
        viewset = views.RegistrationViewSet()
        resp = viewset.create(request)
        self.assertEqual(resp.status_code, 400)
        jsonResp = json.loads(resp.data.decode('utf-8'))
        self.assertIn('errors', jsonResp)
        self.assertEqual(jsonResp['errors'][0], 'Invalid Request')
    
    def test_missing_password_create_user(self):
        user_dict = self.user_dict.copy()
        user_dict.pop('password')
        request = self.factory.post('/auth/register', user_dict)
        viewset = views.RegistrationViewSet()
        resp = viewset.create(request)
        self.assertEqual(resp.status_code, 400)
        jsonResp = json.loads(resp.data.decode('utf-8'))
        self.assertIn('errors', jsonResp)
        self.assertEqual(jsonResp['errors'][0], 'Invalid Request')
    
    def test_invalid_body_create_user(self):
        request = self.factory.post('/auth/register', self.user_dict)
        viewset = views.RegistrationViewSet()
        resp = viewset.create(request)
        self.assertEqual(resp.status_code, 400)
        jsonResp = json.loads(resp.data.decode('utf-8'))
        self.assertIn('errors', jsonResp)
        self.assertEqual(jsonResp['errors'][0], 'Invalid Request')
            
    def test_create_user(self):
        # Valid posts must use application/json for the content-type
        request = self.factory.post('/auth/register', self.user_dict, content_type='application/json')
        viewset = views.RegistrationViewSet()
        resp = viewset.create(request)
        self.assertEqual(resp.status_code, 201)
        self.createJsonResp = json.loads(resp.data.decode('utf-8'))
        self.assertIn('user', self.createJsonResp)
        self.assertIn('refresh', self.createJsonResp)
        self.assertIn('token', self.createJsonResp)
        self.assertRegex(self.createJsonResp['token'], r'^[a-zA-Z][a-zA-Z0-9\.]')
        self.assertRegex(self.createJsonResp['refresh'], r'^[a-zA-Z][a-zA-Z0-9\.]')
        userData = self.createJsonResp['user']
        self.assertEqual(userData['id'], self.user_id)
        self.assertTrue(userData['is_active'])
        self.assertRegex(userData['token'], r'^[0-9]{6}$')
    
    def test_refresh_token(self):
        self.user_id = 2
        self.test_create_user()
        request = self.factory.post(
            '/auth/refresh', 
            self.createJsonResp,
            content_type='application/json'
        )
        viewset = views.RefreshViewSet()
        resp = viewset.create(request)
        self.assertEqual(resp.status_code, 200)
        jsonResp = json.loads(resp.data.decode('utf-8'))
        self.assertListEqual(['access', 'refresh'], list(jsonResp.keys()))
    
    def test_refresh_invalid_token_format(self):
        refresh = 'xxxx'
        request = self.factory.post(
            '/auth/refresh', 
            {'refresh': refresh}, 
            content_type='application/json'
        )
        viewset = views.RefreshViewSet()
        self.assertRaises(InvalidToken, viewset.create, request)

    def test_refresh_invalid_token(self):
        refresh = 'xxxx.xxxx'
        request = self.factory.post(
            '/auth/refresh',
            {'refresh': refresh},
            content_type='application/json'
        )
        viewset = views.RefreshViewSet()
        self.assertRaises(InvalidToken, viewset.create, request)
