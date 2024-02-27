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
    
    def test_create_user(self):
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

        view = views.UserViewSet(request)
        view.get_queryset

        resp = viewset.create(request)
        self.assertEqual(resp.status_code, 404)
        jsonResp = json.loads(resp.content.decode('utf-8'))
        self.assertIn('errors', jsonResp)
        self.assertEqual(jsonResp['errors'][0], 'Invalid Request') 

    def test_get_object(self):
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