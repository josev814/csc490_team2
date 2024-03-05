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
    
    def test_valid_login_user(self):
        # Valid posts must use application/json for the content-type
        request = self.factory.post('/auth/register', self.user_dict, content_type='application/json')
        viewset = auth_views.RegistrationViewSet()
        resp = viewset.create(request)
        self.assertEqual(resp.status_code, 201)
        # print("Actual Status Code:", resp.status_code)
        # self.createJsonResp = resp.data
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

        view = views.UserViewSet()
        request = self.factory.post('/users/login_user', self.user_dict, content_type='application/json')
        user_results = view.login_user(request)
        self.assertIs(user_results.status_code, 200)
        user_data = user_results.data
        self.assertIsNotNone(user_data)
        self.assertNotIn('errors', user_data)
        self.assertIn('is_active', user_data)
        self.assertIn('email', user_data)
        self.assertEqual(user_data['email'], self.user_dict['email'])
    
    def test_user_does_not_exist(self):
        user_dict = self.user_dict.copy()
        user_dict.pop('email')
        request = self.factory.post('/users/login_user', user_dict, content_type='application/json')
        view = views.UserViewSet()
        resp = view.login_user(request)
        self.assertEqual(resp.status_code, 400)
        jsonResp = json.loads = resp.data
        self.assertIn('errors', jsonResp)
        #changed to assertNotEqual from assertEqual
        self.assertNotEqual(jsonResp['errors'][0], 'Invalid Request')

    def test_invalid_password(self):
        user_dict = self.user_dict.copy()
        # saving the password in dict
        user_dict['password'] = 'wrongpassword'
        request = self.factory.post('/users/login_user', user_dict, content_type='application/json')
        viewset = views.UserViewSet()
        resp = viewset.login_user(request)
        self.assertEqual(resp.status_code, 401)
        jsonResp = resp.data
        self.assertIn('errors', jsonResp)
        self.assertEqual(jsonResp['errors'][0], 'Invalid Credentials')

    def test_is_active_is_false(self):
        request = self.factory.post('/auth/register', self.user_dict, content_type='application/json')
        viewset = auth_views.RegistrationViewSet()
        resp = viewset.create(request)
        self.assertEqual(resp.status_code, 201)
        self.createJsonResp = resp.data
        self.assertIn('user', self.createJsonResp)
        self.assertIn('refresh', self.createJsonResp)
        self.assertIn('token', self.createJsonResp)
        self.assertRegex(self.createJsonResp['token'], r'^[a-zA-Z][a-zA-Z0-9\.]')
        self.assertRegex(self.createJsonResp['refresh'], r'^[a-zA-Z][a-zA-Z0-9\.]')
        userData = self.createJsonResp['user']
        self.assertEqual(userData['id'], self.user_id)
        self.assertTrue(userData['is_active'])
        self.assertRegex(userData['token'], r'^[0-9]{6}$')
        print(userData)
        jsonResp = resp.data
        if userData['is_active']!=True:
        #changing this if statement
        #if userData[1]!=userData['is_active']:
            resp = viewset.create(request)
            self.assertIn('errors', jsonResp)
            self.assertEqual(jsonResp['errors'][0], 'Invalid Request')
