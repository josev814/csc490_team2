import json
from django.test import RequestFactory, TestCase

from stocks.views import StockViewSet

# Create your tests here.
class StockTestCases(TestCase):
    symbol = None
    story_types = ['STORY', 'VIDEO']

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.symbol = 'AMZN'

    def tearDown(self) -> None:
        return super().tearDown()

    def test_find_ticker(self):
        request = self.factory.get('/stocks/find/amazon')
        stock_view = StockViewSet()
        self.resp = stock_view.find_ticker(request)
        self.assertIsNotNone(self.resp)
        self.assertEqual(self.resp.status_code, 200)
        json_resp = json.loads(self.resp.content)
        self.assertEqual(json_resp['count'], 7)
        self.assertIn('quotes', json_resp)
        self.assertEqual(len(json_resp['quotes']), 7)
        self.assertIn('symbol', json_resp['quotes'][0])
        self.assertIn(json_resp['quotes'][0]['symbol'], self.symbol)

    def test_get_ticker_news(self):
        request = self.factory.get(f'/stocks/{self.symbol}/news')
        stock_view = StockViewSet()
        resp = stock_view.get_ticker_news(request)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.status_code, 200)
        json_resp = json.loads(resp.content)
        self.assertEqual(json_resp['count'], 20)
        count = json_resp['count']
        self.assertIn('news', json_resp)
        self.assertEqual(len(json_resp['news']), count)
        self.assertIn('type', json_resp['news'][0])
        self.assertIn(json_resp['news'][0]['type'], self.story_types)
    
    def test_get_ticker_metrics(self):
        request = self.factory.get(f'/stocks/{self.symbol}')
        stock_view = StockViewSet()
        resp = stock_view.get_ticker(request, self.symbol)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.status_code, 200)
        json_resp = json.loads(resp.content)
        self.assertIn('chart', json_resp)
        self.assertIn('error', json_resp['chart'])
        self.assertIsNone(json_resp['chart']['error'])
        self.assertIn('result', json_resp['chart'])
        result = json_resp['chart']['result'][0]
        self.assertEqual(result['meta']['symbol'], self.symbol)
