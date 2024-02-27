import json
from django.test import RequestFactory, TestCase
from django.http import JsonResponse


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
    
    def test_get_all_users_when_not_admin(self):
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
        self.assertEquals(userData['id'], self.user_id)
        self.assertFalse(userData['is_active'])
        self.assertRegex(userData['token'], r'^[0-9]{6}$')

        view = views.UserViewSet()
        user_results = view.get_queryset()
        self.assertIsNone(user_results)
    
    def test_valid_login_user(self):
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
        self.assertEquals(userData['id'], self.user_id)
        self.assertFalse(userData['is_active'])
        self.assertRegex(userData['token'], r'^[0-9]{6}$')

        view = views.UserViewSet()
        user_results = view.login_user(request)
        self.assertIsNotNone(user_results)
        self.assertNotIn('errors', user_results)
        self.assertIn('access_token', user_results)
        self.assertIn('refresh_token', user_results)
    
    def test_invalid_login_user_no_email(self):
        # Valid posts must use application/json for the content-type
        user_dict = self.user_dict.copy()
        del user_dict['email']
        request = self.factory.post('/auth/register', user_dict, content_type='application/json')

        view = views.UserViewSet()
        user_results = view.login_user(request)
        self.assertIsNotNone(user_results)
        self.assertIn('errors', user_results)
        self.assertIn(user_results['status_code'], 400)
        


    def test_find_user(self):
        request = self.factory.get('/')
        viewset = views.UserViewSet()
        viewset.request = request
        viewset.lookup_field = 'pk'
        obj = viewset.get_object()
        resp = viewset.create(request)

        self.assertEqual(obj, self)
        self.assertEqual(resp.status_code, 404)
        

    def test_get_object_invalid(self):
        request = self.factory.get('/')
        viewset = views.UserViewSet()
        request.user = self.user
        lookup_value = 9999 
        obj = viewset.get_object()
        resp = viewset.create(request)
        viewset.request = request
        viewset.lookup_field = 'pk'
        self.assertEqual(resp.status_code, 404)

    def test_search(self):
        request = self.factory.get('/')
        request.user = self
        viewset = views.UserViewSet()
        resp = viewset.create(request)
        results = viewset.search('example')
        self.assertIsInstance(results, dict)
        self.assertIn('quotesCount', results)
        self.assertIn('newsCount', results)
        self.assertIn('listsCount', results)


    def test_find_user(self, entry):
        entry.return_value = {'results': ['user1', 'user2']}
        request = self.factory.get('/')
        request.user = views.find_user()
        response = views.find_user(request, 'example')
        entry.assert_called_once_with('example', 'user')
        self.assertIsInstance(response, JsonResponse)
        content = response.content.decode('utf-8')
        self.assertEqual(content, '{"results": ["user1", "user2"]}')