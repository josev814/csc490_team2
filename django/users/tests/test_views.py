import json
from django.test import RequestFactory, TestCase
from django.http import JsonResponse
from auth import views as auth_views


from users import views

# Create your tests here.
class UsersTestCases(TestCase):

    user_dict = {
        'email': 'qwertyuiop@mail.com',
        'password': 'UnitTestingPassword'
    }
    user_id = 1

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def tearDown(self) -> None:
        return super().tearDown()
    
    """ def test_get_all_users_when_not_admin(self):
        # Valid posts must use application/json for the content-type
        request = self.factory.post('/auth/register', self.user_dict, content_type='application/json')
        viewset = views.UserViewSet()
        resp = viewset.create(request)
        self.assertEqual(resp.status_code, 201)
        self.createJsonResp = json.loads(resp.content.decode('utf-8'))
        self.assertIn('user', self.createJsonResp)
        self.assertIn('refresh', self.createJsonResp)
        self.assertIn('token', self.createJsonResp)
        self.assertRegex(self.createJsonResp['token'], r'^[a-zA-Z][a-zA-Z0-9\.]')
        self.assertRegex(self.createJsonResp['refresh'], r'^[a-zA-Z][a-zA-Z0-9\.]')
        userData = self.createJsonResp['user']
        self.assertEqual(userData['id'], self.user_id)
        self.assertFalse(userData['is_active'])
        self.assertRegex(userData['token'], r'^[0-9]{6}$') 

        view = views.UserViewSet()
        user_results = view.get_queryset()
        self.assertIsNone(user_results) """
    
    def test_valid_login_user(self):
        # Valid posts must use application/json for the content-type
        request = self.factory.post('/auth/register', self.user_dict, content_type='application/json')
        viewset = auth_views.RegistrationViewSet()
        resp = viewset.create(request)
        self.assertEqual(resp.status_code, 201)
        self.createJsonResp = json.loads(resp.content.decode('utf-8'))
        self.assertIn('user', self.createJsonResp)
        self.assertIn('refresh', self.createJsonResp)
        self.assertIn('token', self.createJsonResp)
        self.assertRegex(self.createJsonResp['token'], r'^[a-zA-Z][a-zA-Z0-9\.]')
        self.assertRegex(self.createJsonResp['refresh'], r'^[a-zA-Z][a-zA-Z0-9\.]')
        userData = self.createJsonResp['user']
        self.assertEqual(userData['id'], self.user_id)
        self.assertTrue(userData['is_active'])
        self.assertRegex(userData['token'], r'^[0-9]{6}$')

        view = views.UserViewSet()
        request = self.factory.post('/users/login', self.user_dict, content_type='application/json')
        user_results = view.login_user(request)
        self.assertIs(user_results.status_code, 200)
        user_data = user_results.data
        self.assertIsNotNone(user_data)
        self.assertNotIn('errors', user_data)
        self.assertIn('is_active', user_data)
        self.assertIn('email', user_data)
        self.assertEqual(user_data['email'], self.user_dict['email'])
    
    # def test_invalid_login_user_no_email(self):
    #     # Valid posts must use application/json for the content-type
    #     user_dict = self.user_dict.copy()
    #     del user_dict['email']
    #     request = self.factory.post('/auth/register', user_dict, content_type='application/json')

    #     view = views.UserViewSet()
    #     user_results = view.login_user(request)
    #     self.assertIsNotNone(user_results)
    #     self.assertIn('errors', user_results)
    #     self.assertIn(user_results['status_code'], 400)

    # def test_invalid_login_user_no_password(self):
    #     user_dict = self.user_dict.copy()
    #     del user_dict['password ']
    #     request = self.factory.post('/auth/register', user_dict, content_type='application/json')

    #     view = views.UserViewSet()
    #     user_results = view.login_user(request)
    #     self.assertIsNotNone(user_results)
    #     self.assertIn('errors', user_results)
    #     self.assertIn(user_results['status_code'], 400)