"""
Logic for the stocks app
"""
from datetime import datetime, timedelta
import requests

from rest_framework import viewsets, status, filters
#from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
#from rest_framework.decorators import api_view
from rest_framework.response import Response

from stocks.serializers import StockSerializer, StockSearchSerializer, StockDataSerializer
from stocks.models import Stocks, StockSearch, StockData

from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

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
    starttime=int(datetime.now().timestamp()) - ( 86400 * 7 )
    endtime=int(datetime.now().timestamp())

    def build_params(self, param_dict:dict) -> str:
        """
        This builds out the parameters required for the url
        """
        params = ''
        # merge dicts
        param_dict = param_dict | self.extra_params
        separator=False
        for item in param_dict.items():
            if separator:
                params += '&'
            params += f'{item[0]}={item[1]}'
            separator=True
        return params

    def search(self, search_param:str, retrieve:str='quotes', limit=20) -> dict:
        """
        This method allows to search for a string or symbol and return the results
        
        params: retrieve str options are quotes, news, lists
        """
        params = {
            'q': search_param,
            'quotesCount': 0,
            'newsCount': 0,
            'listsCount': 0,
        }
        #override default
        params[f'{retrieve}Count'] = limit
        query_params = self.build_params(params)
        query_uri = f'{self.base_url}search?{query_params}'
        return self.__make_request(query_uri)

    def get_chart(self, ticker:str, interval:str='1m', 
                  period1:int=starttime, period2:int=endtime) -> dict:
        """
        Gets chart metrics for a symbol

        param: interval: str values: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, ytd, max
        param: period1 int The start of the data we want. This should be an int based on a timestamp
        param: period2 int The end of the data we want. This should be an int based on a timestamp
        """
        params = {
            'interval': interval,
            'includePrePost': True
        }
        if period1:
            params['period1'] = period1
        if period2:
            params['period2'] = period2
        query_params = self.build_params(params)
        base_url = self.base_url.replace("/v1/", "/v8/")
        query_uri = f'{base_url}chart/{ticker}?{query_params}'
        return self.__make_request(query_uri)

    def __make_request(self, query_uri) -> dict:
        """
        This performs the request to the yahoo api and returns the json result
        """
        r = requests.get(
            query_uri,
            headers=self.headers,
            timeout=5
        )
        if r.status_code != 200:
            bad_result = {
                'error': f'Failed retrieving reponse from Yahoo Finance for {query_uri}',
                'status_code': r.status_code
            }
            return bad_result
        return r.json()        


class StockViewSet(viewsets.ModelViewSet):
    """The User ViewSet that queries the Users database

    :param viewsets: The ModelViewSet, so we can access the db
    :type viewsets: class
    :return: Returns the Viewset for stocks
    :rtype: viewset
    """
    http_method_names = ['get']
    queryset = Stocks.objects.all().order_by('-ticker')
    serializer_class = StockSerializer
    filter_backends = [filters.OrderingFilter]
    #permission_classes = [IsAuthenticated,]
    ordering_fields = ['ticker', 'name']
    ordering = ['-ticker', '-name']

    def __find_save_ticker(self, ticker:str) -> list:
        yf = YahooFinance()
        results = yf.search(ticker)
        stock_search = StockSearch()
        save_search_results = stock_search.save_search_results(results)
        if save_search_results['errors'] is not None:
            return [False, save_search_results]
        save_search_request = stock_search.save_search_request(ticker)
        if save_search_request['errors'] is not None:
            return [False, save_search_request]
        return [True, None]

    @method_decorator(cache_page(60 * 60 * 24))  # cache for 24 hours
    @action(detail=False, methods=['get'])
    def find_ticker(self, request):
        """
        This endpoint allows us to search for a ticker using the search parameter
        """
        if 'ticker' not in request.query_params:
            return Response(
                {
                    'errors': [{'Missing required parameter "ticker"'}]
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        find = request.query_params['ticker']
        stock_search = StockSearch()
        if not stock_search.does_search_record_exist(find, None):
            saved, respose = self.__find_save_ticker(find)
            if not saved:
                return Response(respose, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        kwsearch = Q(ticker__istartswith=find.lower()) | Q(name__istartswith=find.lower())
        stocks_qs = Stocks.objects.filter(kwsearch)[:20]
        stock_data = StockSerializer(
            instance=stocks_qs,
            many=True,
            context={'request': request}
        ).data
        return Response({
            'count': len(stock_data),
            'errors': None,
            'records': stock_data
        }, status=status.HTTP_200_OK)

    @method_decorator(cache_page(60 * 60 * 24))  # cache for 24 hours
    @action(detail=False, methods=['GET'])
    def get_ticker_news(self, request):
        """
        Gets a ticker's chart data
        """
        if 'ticker' not in request.query_params:
            return Response(
                {
                    'errors': [{'Missing required parameter "ticker"'}]
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        ticker = request.query_params.get('ticker')
        yf = YahooFinance()
        results = yf.search(ticker, 'news')
        return Response(results)

    @method_decorator(cache_page(60 * 60 * 1))  # cache for 24 hours
    @action(detail=False, methods=['GET'])
    def get_ticker_metrics(self, request):
        """
        Gets a ticker's chart data
        """
        if 'ticker' not in request.query_params:
            return Response(
                {
                    'errors': [{'Missing required parameter "ticker"'}]
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        optional_keys=['starttime','endtime','interval']
        kwargs = self.__get_optional_query_params(request, optional_keys)
        ticker = request.query_params.get('ticker')

        stock_search = StockSearch()
        if not stock_search.does_search_record_exist(ticker, None):
            saved, respose = self.__find_save_ticker(ticker)
            if not saved:
                return Response(respose, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        delta='days'
        interval=1
        if 'interval' in kwargs and kwargs['interval'] == '1m':
            delta='minutes'
            interval=5
            stock_search.set_search_refresh(delta, interval)  # refresh every 5 minutes
        search_qs = stock_search.get_search_record(ticker, kwargs)
        search_record = StockSearchSerializer(
            instance=search_qs,
            many=True,
            context={'request': request}
        ).data
        if search_record is not None:
            yf = YahooFinance()
            results = yf.get_chart(ticker, **kwargs)
            save_search_results = stock_search.save_search_results(results)
            if save_search_results['errors'] is not None:
                return Response(save_search_results, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            save_search_request = stock_search.save_search_request(ticker, kwargs)
            if save_search_request['errors'] is not None:
                return Response(save_search_request, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            search_qs = stock_search.get_search_record(ticker, kwargs)
            search_record = StockSearchSerializer(
                instance=search_qs,
                many=True,
                context={'request': request}
            ).data
        last_updated = search_record[0]['updated_date']
        next_update = datetime.fromisoformat(last_updated) + timedelta(**{delta:interval})
        ticker_filter = Q(ticker__iexact=ticker.lower())
        ticker_pk = Stocks.objects.filter(ticker_filter)[0].pk
        kwsearch = Q(ticker=ticker_pk)
        for kwfilter in kwargs:
            if kwfilter == 'internavl':
                kwsearch &= Q(granularity=kwargs[kwfilter])
            elif kwfilter == 'starttime':
                kwsearch &= Q(timestamp__gte=kwargs[kwfilter])
            elif kwfilter == 'endtime':
                kwsearh &= Q(timestamp__lte=kwargs[kwfilter])
        stockdata_qs = StockData.objects.filter(kwsearch)[:20]
        stock_data = StockDataSerializer(
            instance=stockdata_qs,
            many=True,
            context={'request': request}
        ).data
        return Response({
            'count': len(stock_data),
            'errors': None,
            'refresh': {
                'last_refresh': last_updated,
                'next_refresh':next_update
            },
            'records': stock_data
        }, status=status.HTTP_200_OK)

    def __get_optional_query_params(self, request, keys):
        kwargs = {}
        key_replacements = {
            'starttime': 'period1',
            'endtime': 'period2',
        }
        for item in keys:
            if item in request.query_params:
                if item in key_replacements.keys():
                    kwargs[key_replacements[item]] = request.query_params.get(item)
                else:
                    kwargs[item] = request.query_params.get(item)
        return kwargs
