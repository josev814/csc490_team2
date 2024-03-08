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
    
    def __mock_get_request(self, url, query_params: dict) -> RequestFactory:
        request = self.factory.get(url, content_type='application/json')
        request.query_params = query_params
        return request
        

    def test_find_ticker(self):
        query_params={'ticker':'amazon'}
        request = self.__mock_get_request('/stocks/find_ticker/', query_params)
        stock_view = StockViewSet()
        self.resp = stock_view.find_ticker(request)
        self.assertIsNotNone(self.resp)
        self.assertEqual(self.resp.status_code, 200)
        json_resp = self.resp.data
        self.assertEqual(json_resp['count'], 7)
        self.assertIn('records', json_resp)
        self.assertEqual(len(json_resp['records']), 7)
        self.assertIn('ticker', json_resp['records'][0])
        self.assertIn(json_resp['records'][0]['ticker'], self.symbol)

    def test_get_ticker_news(self):
        query_params={'ticker':self.symbol}
        request = self.__mock_get_request(f'/stocks/get_ticker_news/', query_params)
        stock_view = StockViewSet()
        resp = stock_view.get_ticker_news(request)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.status_code, 200)
        json_resp = resp.data
        self.assertEqual(json_resp['count'], 20)
        count = json_resp['count']
        self.assertIn('news', json_resp)
        self.assertEqual(len(json_resp['news']), count)
        self.assertIn('type', json_resp['news'][0])
        self.assertIn(json_resp['news'][0]['type'], self.story_types)
    
    def test_get_ticker_metrics(self):
        query_params = {'ticker': self.symbol}
        request = self.__mock_get_request(f'/stocks/get_ticker_metrics/', query_params)
        stock_view = StockViewSet()
        resp = stock_view.get_ticker_metrics(request)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.status_code, 200)
        json_resp = resp.data
        self.assertIn('errors', json_resp)
        self.assertIsNone(json_resp['errors'])
        self.assertIn('records', json_resp)
        first_record = json_resp['records'][0]
        self.assertGreaterEqual(first_record['high'], 1)
        self.assertEqual(first_record['granularity'], '1m')
    
    def test_missing_ticker_in_request_for_search(self):
        query_params = {}
        request = self.__mock_get_request(f'/stocks/find_ticker/', query_params)
        stock_view = StockViewSet()
        resp = stock_view.find_ticker(request)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.status_code, 400)
        json_resp = resp.data
        self.assertIn('errors', json_resp)
        self.assertIsNotNone(json_resp['errors'])
        self.assertIn('Missing required', json_resp['errors'][0])

    def test_missing_ticker_in_request_for_news(self):
        query_params = {}
        request = self.__mock_get_request(f'/stocks/get_ticker_news/', query_params)
        stock_view = StockViewSet()
        resp = stock_view.get_ticker_news(request)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.status_code, 400)
        json_resp = resp.data
        self.assertIn('errors', json_resp)
        self.assertIsNotNone(json_resp['errors'])
        self.assertIn('Missing required', json_resp['errors'][0])
    
    def test_missing_ticker_in_request_for_metrics(self):
        query_params = {}
        request = self.__mock_get_request(f'/stocks/get_ticker_metrics/', query_params)
        stock_view = StockViewSet()
        resp = stock_view.get_ticker_metrics(request)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.status_code, 400)
        json_resp = resp.data
        self.assertIn('errors', json_resp)
        self.assertIsNotNone(json_resp['errors'])
        self.assertIn('Missing required', json_resp['errors'][0])
    
    def test_metric_interval(self):
        query_params = {
            'ticker': 'amzn',
            'interval': '5m',
            'starttime': 1708114200,
            'endtime': 1709517600
        }
        request = self.__mock_get_request(f'/stocks/get_ticker_metrics/', query_params)
        stock_view = StockViewSet()
        resp = stock_view.get_ticker_metrics(request)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.status_code, 200)
        json_resp = resp.data
        self.assertIn('errors', json_resp)
        self.assertIsNone(json_resp['errors'])
        self.assertIn('records', json_resp)
        first_record = json_resp['records'][0]
        self.assertGreaterEqual(first_record['high'], 169)
        self.assertEqual(first_record['granularity'], '5m')
    