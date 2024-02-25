import json
from django.test import RequestFactory, TestCase

from users import views

# Create your tests here.
class UsersTestCases(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_find_undefined_user(self):
        pass
        # request = self.factory.get('/users/find/')
        # self.resp = views.find_user(request)
        # self.assertIsNotNone(self.resp)
        # self.assertEqual(self.resp.status_code, 200)
        # json_resp = json.loads(self.resp.content)
        # self.assertEqual(json_resp['count'], 0)
        # self.assertEqual(json_resp['errors'], 'Missing User ID')

    def test_find_missing_user(self):
        pass
        # request = self.factory.get('/users/find/xxx')
        # self.resp = views.find_user(request)
        # self.assertIsNotNone(self.resp)
        # self.assertEqual(self.resp.status_code, 200)
        # json_resp = json.loads(self.resp.content)
        # self.assertEqual(json_resp['count'], 0)
        # self.assertEqual(json_resp['errors'], 'User does not exist')
