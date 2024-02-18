from django.test import TestCase
from django.http import JsonResponse

from stocks import views

# Create your tests here.
class StockTests(TestCase):
    component = None
    resp = None

    def setup(self) -> None:
        self.component = views()
        self.resp = self.component.get_ticker('amzn')

    def tearDown(self) -> None:
        return super().tearDown()

    def test_find_ticker(self):
        self.setUp()
        self.assertEqual(self.resp.status_code, 200)
        json_resp = self.resp.json()
        self.assertEqual(json_resp['count'], 7)
        self.assertIn(json_resp, 'quotes')
        self.assertIn(json_resp['quotes'][0]['symbol'], 'AMZN')
