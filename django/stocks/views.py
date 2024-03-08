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
            saved, response = self.__find_save_ticker(find)
            if not saved:
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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

    def _stock_searching(self, request, ticker):
        """Saves the stock search record for a symbol

        :param request: _description_
        :type request: _type_
        :param ticker: _description_
        :type ticker: _type_
        :return: _description_
        :rtype: _type_
        """
        stock_search = StockSearch()
        search_qs = stock_search.get_search_record(ticker, None)
        search_records = StockSearchSerializer(
            instance=search_qs,
            many=True,
            context={'request': request}
        )
        if search_records is None or not search_records or len(search_records.data) == 0:
            saved, response = self.__find_save_ticker(ticker)
            if not saved:
                return [
                    False, 
                    Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                ]
        return [True, None]
    
    def _find_yahoo_data_and_save(self, request, ticker, kwargs):
        """
        Finds the yahoo chart data requested and saves its search and metrics
        """
        stock_search = StockSearch()
        yf = YahooFinance()
        results = yf.get_chart(ticker, **kwargs)
        save_search_results = stock_search.save_search_results(results)
        if save_search_results['errors'] is not None:
            return [
                False,
                Response(save_search_results, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            ]
        save_search_request = stock_search.save_search_request(ticker, kwargs)
        if save_search_request['errors'] is not None:
            return [
                False,
                Response(save_search_request, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            ]
        search_qs = stock_search.get_search_record(ticker, kwargs)
        search_records = StockSearchSerializer(
            instance=search_qs,
            many=True,
            context={'request': request}
        )
        return [True, search_records]

    def _get_ticker_primary_key(self, ticker):
        """
        Returns the primary key of a ticker
        """
        ticker_filter = Q(ticker__iexact=ticker.lower())
        return Stocks.objects.filter(ticker_filter)[0].pk

    #@method_decorator(cache_page(60 * 60 * 1))  # cache for 24 hours
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
        optional_keys = ['starttime','endtime','interval']
        kwargs = self.__get_optional_query_params(request, optional_keys)
        ticker = request.query_params.get('ticker')

        succ, resp = self._stock_searching(request, ticker)
        if not succ:
            return resp
        
        stock_search = StockSearch()
        delta_interval = {'delta_name': 'days', 'delta_value': 1}
        if 'interval' in kwargs and kwargs['interval'] == '1m':
            delta_interval = {'delta_name': 'minutes', 'delta_value': 5}
            stock_search.set_search_refresh(**delta_interval)  # refresh every 5 minutes
        search_records = StockSearchSerializer(
            instance = stock_search.get_search_record(ticker, kwargs),
            many=True,
            context={'request': request}
        )
        if search_records is None or not search_records or len(search_records.data) == 0:
            succ, resp = self._find_yahoo_data_and_save(request, ticker, kwargs)
            if not succ:
                return resp
            search_records = resp
            if search_records is None or not search_records or len(search_records.data) == 0:
                return Response({'errors': ['Yahoo Finance data was not successfully saved']})
        refresh = {
            'last_refresh': search_records.data[-1]['updated_date']
        }
        refresh['next_refresh'] = datetime.fromisoformat(refresh['last_refresh']) + \
            timedelta(**{delta_interval['delta_name']:delta_interval['delta_value']})
        kwsearch = Q(ticker = self._get_ticker_primary_key(ticker))
        for kwfilter in kwargs:
            if kwfilter == 'internval':
                kwsearch &= Q(granularity=kwargs.get(kwfilter))
            elif kwfilter == 'starttime':
                kwsearch &= Q(timestamp__gte=kwargs.get(kwfilter))
            elif kwfilter == 'endtime':
                kwsearch &= Q(timestamp__lte=kwargs.get(kwfilter))
        stock_data = StockDataSerializer(
            instance = StockData.objects.filter(kwsearch)[:20],
            many=True,
            context={'request': request}
        ).data
        return Response({
            'count': len(stock_data),
            'errors': None,
            'refresh': refresh,
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
                if item in key_replacements:
                    kwargs[key_replacements[item]] = request.query_params.get(item)
                else:
                    kwargs[item] = request.query_params.get(item)
        return kwargs
