import json
from django.test import RequestFactory, TestCase
from django.http import JsonResponse
from auth import views as auth_views


from users import views, models


class UsersTestCases(TestCase):

    user_dict = {
        'email': 'qwertyuiop@mail.com',
        'password': 'UnitTestingPassword'
    }
    user_id = 3

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_missing_email_create_user(self):
        user_dict = self.user_dict.copy()
        user_dict.pop('email')
        request = self.factory.post('/auth/register', user_dict)
        viewset = models.UserManager()
        resp = viewset.create(request)
        self.assertEqual(resp.status_code, 400)
        jsonResp = json.loads(resp.content.decode('utf-8'))
        self.assertIn('errors', jsonResp)
        self.assertEqual(jsonResp['errors'][0], 'Invalid Request')
    
    def test_missing_password_create_user(self):
        user_dict = self.user_dict.copy()
        user_dict.pop('password')
        request = self.factory.post('/auth/register', user_dict)
        viewset = models.UserManager()
        resp = viewset.create(request)
        self.assertEqual(resp.status_code, 400)
        jsonResp = json.loads(resp.content.decode('utf-8'))
        self.assertIn('errors', jsonResp)
        self.assertEqual(jsonResp['errors'][0], 'Invalid Request')