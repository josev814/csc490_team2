from django.test import TestCase
from django.urls import reverse

class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('users/')
        self.user={
            'email':'testemail@gmail.com',
            'username':'username',
            'password':'password',
            'password2':'password',
            'name':'fullname'
        }
        self.user_short_password={
            'email':'testemail@gmail.com',
            'username':'username',
            'password':'tes',
            'password2':'tes',
            'name':'fullname'
        }
        self.user_unmatching_password={
            'email':'testemail@gmail.com',
            'username':'username',
            'password':'teslatt',
            'password2':'teslatto',
            'name':'fullname'
        }
        self.user_invalid_email={
            'email':'test.com',
            'username':'username',
            'password':'teslatt',
            'password2':'teslatto',
            'name':'fullname'
        }
        return super().setUp()
    
class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        reponse=self.client.get(self.register_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'auth/users')

    def test_can_register_user(self):
        response=self.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)

    def test_cant_register_user_withshortpassword(self):
        response=self.post(self.register_url,self.user_short_password,format='text/html')
        self.assertEqual(response.status_code,400)

    def test_cant_register_user_with_unmatching_passwords(self):
        response=self.post(self.register_url,self.user_unmatching_password,format='text/html')
        self.assertEqual(response.status_code,400)
    
    def test_cant_register_user_with_invalid_email(self):
        response=self.post(self.register_url,self.user_invalid_email,format='text/html')
        self.assertEqual(response.status_code,400)

    def test_cant_register_user_taken_email(self):
        self.client.post(self.register_url,self.user,format='text/html')
        response=self.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,400)