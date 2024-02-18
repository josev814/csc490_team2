"""
Logic for the stocks app
"""
#from django.shortcuts import render
from django.http import JsonResponse
import requests

class YahooFinance:
    """
    This class is for making requests to Yahoo Finance's API
    """

    base_url = 'https://query1.finance.yahoo.com/v1/finance/'
    extra_params = {
        'lang': 'en-Us',
        'region': 'US'
    }
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'AppleWebKit/537.36 (KHTML, like Gecko)',
        'Chrome/121.0.0.0',
        'Safari/537.36',
        'Edg/121.0.0.0'
    ]
    headers = {
        'User-Agent': ' '.join(user_agents)
    }

    def build_params(self, param_dict:dict) -> str:
        """
        This builds out the parameters required for the url
        """
        params = ''
        # merge dicts
        param_dict = param_dict | self.extra_params
        for item in param_dict.items():
            params += f'&{item[0]}={item[1]}'
        return params

    def search(self, search_param:str, retrieve:str='quotes', limit=20) -> dict:
        """
        This method allows to search for a string or symbol and return the results
        
        params: retrieve str options are quotes, news, lists
        """
        params = {
            'quotesCount': 0,
            'newsCount': 0,
            'listsCount': 0,
        }
        #override default
        params[f'{retrieve}Count'] = limit
        query_params = self.build_params(params)
        query_uri = f'{self.base_url}search?q={search_param}{query_params}'
        return self.__make_request(query_uri)

    def get_chart(self, ticker:str, interval:str='1d', 
                  starttime:int|None=None, endtime:int|None=None) -> dict:
        """
        Gets chart metrics for a symbol

        param: interval: str values: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, ytd, max
        param: starttime int This should be an int based on a timestamp
        param: endtime int This should be an int based on a timestamp
        """
        params = {
            'includePrePost': True
        }
        if starttime:
            params['starttime'] = starttime
        if endtime:
            params['endtime'] = endtime
        query_params = self.build_params(params)
        query_uri = f'{self.base_url}chart/{ticker}?interval={interval}{query_params}'
        return self.__make_request(query_uri)

    def __make_request(self, query_uri) -> dict:
        """
        This performs the request to the yahoo api and returns the json result
        """
        r = requests.get(
            query_uri,
            headers=self.headers
        )
        if r.status_code != 200:
            bad_result = {
                'error': 'Failed retrieving reponse from Yahoo Finance',
                'status_code': r.status_code
            }
            return bad_result
        return r.json()        

# Create your views here.
def index(request):
    """
    This is the main endpoint that gets hit
    """
    print(request)
    resp = {
        'error': {
            'msg': 'Unauthorized Access',
            'status_code': '403'
        }
    }
    return JsonResponse(resp)

def find_ticker(request, search: str='amazon'):
    """
    This endpoint allows us to search for a ticker using the search parameter
    """
    print(request)
    yf = YahooFinance()
    results = yf.search(search)
    return JsonResponse(results)

def get_ticker_news(request, symbol: str='amazon'):
    """
    Gets a ticker's chart data
    """
    print(request)
    yf = YahooFinance()
    results = yf.search(symbol, 'news')
    return JsonResponse(results)

def get_ticker(request, symbol:str):
    """
    Gets a ticker's chart data
    """
    print(request)
    yf = YahooFinance()
    results = yf.get_chart(symbol)
    return JsonResponse(results)
