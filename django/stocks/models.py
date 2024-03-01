"""
Models for the application are stored here
"""
from datetime import datetime, timedelta

from django.db import models, IntegrityError


class Stocks(models.Model):
    """
    Model for a Stocks table
    """
    ticker = models.CharField(max_length=12)
    name = models.CharField(max_length=75)
    exchange_name = models.CharField(max_length=50)
    exchange = models.CharField(max_length=10)
    stock_type = models.CharField(max_length=12)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        """
        Adding indexes for the table
        """
        indexes = [
            models.Index(fields=['ticker', 'name'])
        ]

    def __str__(self):
        """Default return of the class

        :return: Returns the ticker
        :rtype: str
        """
        return f'{self.ticker}'

    def save_search_results(self, yahoo_data:dict) -> dict:
        records = []
        try:
            for entry in yahoo_data:
                record = {
                    'ticker': entry['symbol'],
                    'name': entry['longname'],
                    "exchange": entry['exchange'],
                    "exchange_name": entry['exchDisp'],
                    'stock_type': entry['typeDisp']
                }
                records.append(record)
                existing_tickers = set(Stocks.objects.values_list('ticker', flat=True))
                unique_records = [r for r in records if r['ticker'] not in existing_tickers]
                if unique_records:
                    Stocks.objects.bulk_create([Stocks(**record) for record in unique_records])
        except KeyError as e:
            error = f'KeyError when attempting to save stock results: {e}'
            return {'status': False, 'errors': error}
        except IntegrityError as e:
            error = f'IntegrityError when attempting to save stock results: {e}'
            return {'status': False, 'errors': error}
        return {'status': True, 'errors': None}



class StockData(models.Model):
    """
    Model for the stock data
    """
    ticker = models.ForeignKey(
        'Stocks',
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(auto_now=True)
    high = models.FloatField(default=0.0, max_length=28)
    low = models.FloatField(default=0.0, max_length=28)
    open = models.FloatField(default=0.0, max_length=28)
    close = models.FloatField(default=0.0, max_length=28)
    granularity = models.CharField(max_length=4)
    create_date = models.DateTimeField(auto_now_add=True)
    
    def save_stock_results(self, yahoo_data:dict) -> bool:
        """Parses the yahoo chart results and saves the results to our database

        :param yahoo_data: The yahoo chart results
        :type yahoo_data: dict
        :return: Returns if we were able to successfully save the record
        :rtype: bool
        """
        records = []
        try:
            ticker = yahoo_data['meta']['symbol']
            granularity = yahoo_data['meta']['dataGranularity']
            for i in range(len(yahoo_data['timestamp'])):
                quote_volumes = yahoo_data['indicators']['quote'][0]['volume']
                records.append(
                    {
                        'ticker_id': ticker,
                        'granularity': granularity,
                        'timestamp': datetime.fromtimestamp(yahoo_data['timestamp'][i]),
                        'high': quote_volumes['high'][i],
                        'low': quote_volumes['low'][i],
                        'open': quote_volumes['open'][i],
                        'close': quote_volumes['close'][i]
                    }
                )
            StockData.objects.bulk_create([StockData(**record) for record in records])
            return True
        except KeyError as e:
            print(f'KeyError when attempting to save stock results: {e}')
            return False
        except IntegrityError as e:
            print(f'IntegrityError when attempting to save stock results: {e}')
            return False



class StockSearch(models.Model):
    """
    Stores historical searches for Yahoo
    """
    search_phrase = models.CharField(max_length=128)
    search_args = models.CharField(max_length=1024, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    one_day_ago = datetime.now() - timedelta(days=1)


    class Meta:
        """
        Adding indexes for the table
        """
        indexes = [
            models.Index(fields=['search_phrase', 'search_args'])
        ]
    
    def does_search_record_exist(self, phrase:str, args:str) -> bool:
        """Determines is the search to Yahoo exists or not

        :param phrase: The ticker or company that is being searched for
        :type phrase: str
        :param args: The arguments passed to yahoo
        :type args: str
        :return: Returns if the record existed or not
        :rtype: bool
        """
        search_filter = {
            'search_phrase': phrase,
            'search_args': args,
            'updated_date__gte': self.one_day_ago
        }
        records = StockSearch.objects.filter(**search_filter).count()
        return records > 0
    
    def save_search_request(self, phrase:str, args:str|None=None) -> dict:
        """Determines is the search to Yahoo exists or not

        :param phrase: The ticker or company that is being searched for
        :type phrase: str
        :param args: Additional arguments passed to yahoo
        :type args: str|None
        :return: Returns if the record was saved
        :rtype: bool
        """
        try:
            kwargs = {
                'search_args': args,
                'search_phrase': phrase
            }
            StockSearch.objects.create(**kwargs)
        except IntegrityError as e:
            return {'status': False, 'IntegrityError': f'Failed to save record: {e}'}
        except Exception as e:
            return {'status': False, 'errors': f'Failed to save record: {e}'}
        return {'status': True, 'errors': None}
    
    def save_search_results(self, yahoo_results: dict) -> dict:
        if 'chart' in yahoo_results:
            return StockData().save_search_results(yahoo_results['chart']['result'][0])
        elif 'quotes' in yahoo_results and len(yahoo_results['quotes']) > 0:
            return Stocks().save_search_results(yahoo_results['quotes'])
        print('Unhandled option in save_search_results')
        return {'status': True, 'errors': None}