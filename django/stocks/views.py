from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests

class yahooFinance:

    base_url = 'https://query1.finance.yahoo.com/v1/finance/'
    extra_params = {
        'lang': 'en-Us',
        'region': 'US'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                        'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                        'Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    def build_params(self, param_dict):
        params = ''
        for key in self.extra_params.keys():
            params += f'&{key}={param_dict.get(key)}'
        for key in param_dict.keys():
            params += f'&{key}={param_dict.get(key)}'
        return params

    def search(self, search_param:str, retrieve:str='quotes', limit=20):
        params = {
            'quotesCount': 0,
            'newsCount': 0,
            'listsCount': 0,
        }
        #override default
        params[f'{retrieve}Count'] = limit
        query_params = self.build_params(params)
        query_uri = f'{self.base_url}search?q={search_param}{query_params}'
        return self._make_request(query_uri)

    def get_chart(self, ticker:str, interval:str='1d', starttime:int|None=None, endtime:int|None=None):
        """
        params: interval: str values: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, ytd, max
        """
        params = {
            'includePrePost': True
        }
        #TODO: Add starttime and endtime to query params
        query_params = self.build_params(params)
        query_uri = f'{self.base_url}chart/{ticker}?interval={interval}{query_params}'
        return self._make_request(query_uri)

    def _make_request(self, query_uri):
        r = requests.get(
            query_uri,
            headers=self.headers
        )
        if r.status_code != 200:
            raise Exception('Failed retrieving reponse from Yahoo Finance')
        return r.json()        

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. The index of pullstocks")

def find_ticker(request, search: str='amazon'):
    yf = yahooFinance()
    results = yf.search(search)
    return JsonResponse(results)

def get_ticker_news(request, symbol: str='amazon'):
    yf = yahooFinance()
    results = yf.search(symbol, 'news')
    return JsonResponse(results)

def get_ticker(request, symbol):
    yf = yahooFinance()
    results = yf.get_chart(symbol)
    return JsonResponse(results)